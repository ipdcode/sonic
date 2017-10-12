"""
http://www.ieee802.org/1/files/public/MIBs/LLDP-MIB-200505060000Z.txt
"""
from enum import Enum, unique

from sonic_ax_impl import mibs, logger
from ax_interface import MIBMeta, ContextualMIBEntry, MIBUpdater, ValueType


@unique
class LLDPRemoteTables(int, Enum):
    """
    REDIS_KEY_NAME <--> OID_INDEX
    """
    lldp_rem_time_mark = 1
    # lldp_rem_local_port_num = 2
    # lldp_rem_index = 3
    lldp_rem_chassis_id_subtype = 4
    lldp_rem_chassis_id = 5
    lldp_rem_port_id_subtype = 6
    lldp_rem_port_id = 7
    lldp_rem_port_desc = 8
    lldp_rem_sys_name = 9
    lldp_rem_sys_desc = 10
    # lldp_rem_sys_cap_supported = 11
    # lldp_rem_sys_cap_enabled = 12


class LLDPUpdater(MIBUpdater):
    def __init__(self):
        super().__init__()

        self.db_conn = mibs.init_db()
        self.reinit_data()

        # cache of interface counters
        # { sai_id -> { 'counter': 'value' } }
        self.lldp_counters = {}
        # call our update method once to "seed" data before the "Agent" starts accepting requests.
        self.update_data()

    def reinit_data(self):
        """
        Subclass update interface information
        """
        self.if_name_map, \
        self.if_alias_map, \
        self.if_id_map, \
        self.oid_sai_map, \
        self.oid_name_map = mibs.init_sync_d_interface_tables(self.db_conn)

    def update_data(self):
        """
        Subclass update data routine. Updates available LLDP counters.
        """

        # establish connection to application database.
        self.db_conn.connect(mibs.APPL_DB)

        self.lldp_counters = {}
        for if_name in self.if_name_map:
            lldp_kvs = self.db_conn.get_all(mibs.APPL_DB, mibs.lldp_entry_table(if_name))
            if not lldp_kvs:
                continue
            self.lldp_counters.update({if_name: lldp_kvs})
        if not self.lldp_counters:
            logger.warning("0 - b'LLDP_ENTRY_TABLE' is empty. No LLDP information could be retrieved.")

    def local_port_id(self, sub_id):
        if_name = self.oid_name_map[sub_id]
        if if_name not in self.lldp_counters:
            # no LLDP data for this interface--we won't report the local interface
            return None
        return self.if_alias_map[if_name]

    def lldp_table_lookup(self, sub_id, table_name):
        if_name = self.oid_name_map[sub_id]
        if if_name not in self.lldp_counters:
            # no LLDP data for this interface
            return None
        counters = self.lldp_counters[if_name]
        _table_name = bytes(getattr(table_name, 'name', table_name), 'utf-8')
        try:
            return counters[_table_name]
        except KeyError as e:
            mibs.logger.warning(" 0 - b'LLDP_ENTRY_TABLE' missing attribute '{}'.".format(e))
            return None

    def lldp_table_lookup_integer(self, sub_id, table_name):
        """
        :param sub_id: Given sub_id
        :param table_name: name of the table to query.
        :return: int(the subtype)
        """
        subtype_str = self.lldp_table_lookup(sub_id, table_name)
        return int(subtype_str) if subtype_str is not None else None


_lldp_updater = LLDPUpdater()

class LLDPLocPortTable(metaclass=MIBMeta, prefix='.1.0.8802.1.1.2.1.3.7'):
    """
    'lldpLocPortTable'
    """
    lldp_updater = _lldp_updater
    if_range = lldp_updater.oid_name_map.keys()

    # lldpLocPortEntry = '1'

    # lldpLocPortNum = '1.1'

    # lldpLocPortIdSubtype = '1.2'

    lldpLocPortId = ContextualMIBEntry('1.3', if_range, ValueType.OCTET_STRING, lldp_updater.local_port_id)

    # lldpLocPortDesc = '1.4'


class LLDPRemTable(metaclass=MIBMeta, prefix='.1.0.8802.1.1.2.1.4.1'):
    """
    lldpRemTable OBJECT-TYPE
    SYNTAX      SEQUENCE OF LldpRemEntry
    MAX-ACCESS  not-accessible
    STATUS      current
    DESCRIPTION
            "This table contains one or more rows per physical network
            connection known to this agent.  The agent may wish to ensure
            that only one lldpRemEntry is present for each local port,
            or it may choose to maintain multiple lldpRemEntries for
            the same local port.

            The following procedure may be used to retrieve remote
            systems information updates from an LLDP agent:

               1. NMS polls all tables associated with remote systems
                  and keeps a local copy of the information retrieved.
                  NMS polls periodically the values of the following
                  objects:
                     a. lldpStatsRemTablesInserts
                     b. lldpStatsRemTablesDeletes
                     c. lldpStatsRemTablesDrops
                     d. lldpStatsRemTablesAgeouts
                     e. lldpStatsRxPortAgeoutsTotal for all ports.

               2. LLDP agent updates remote systems MIB objects, and
                  sends out notifications to a list of notification
                  destinations.

               3. NMS receives the notifications and compares the new
                  values of objects listed in step 1.

                  Periodically, NMS should poll the object
                  lldpStatsRemTablesLastChangeTime to find out if anything
                  has changed since the last poll.  if something has
                  changed, NMS will poll the objects listed in step 1 to
                  figure out what kind of changes occurred in the tables.

                  if value of lldpStatsRemTablesInserts has changed,
                  then NMS will walk all tables by employing TimeFilter
                  with the last-polled time value.  This request will
                  return new objects or objects whose values are updated
                  since the last poll.

                  if value of lldpStatsRemTablesAgeouts has changed,
                  then NMS will walk the lldpStatsRxPortAgeoutsTotal and
                  compare the new values with previously recorded ones.
                  For ports whose lldpStatsRxPortAgeoutsTotal value is
                  greater than the recorded value, NMS will have to
                  retrieve objects associated with those ports from
                  table(s) without employing a TimeFilter (which is
                  performed by specifying 0 for the TimeFilter.)

                  lldpStatsRemTablesDeletes and lldpStatsRemTablesDrops
                  objects are provided for informational purposes."
    ::= { lldpRemoteSystemsData 1 }

    lldpRemEntry OBJECT-TYPE
    SYNTAX      LldpRemEntry
    MAX-ACCESS  not-accessible
    STATUS      current
    DESCRIPTION
            "Information about a particular physical network connection.
            Entries may be created and deleted in this table by the agent,
            if a physical topology discovery process is active."
    INDEX   {
           lldpRemTimeMark,
           lldpRemLocalPortNum,
           lldpRemIndex
    }
    ::= { lldpRemTable 1 }

    LldpRemEntry ::= SEQUENCE {
          lldpRemTimeMark           TimeFilter,
          lldpRemLocalPortNum       LldpPortNumber,
          lldpRemIndex              Integer32,
          lldpRemChassisIdSubtype   LldpChassisIdSubtype,
          lldpRemChassisId          LldpChassisId,
          lldpRemPortIdSubtype      LldpPortIdSubtype,
          lldpRemPortId             LldpPortId,
          lldpRemPortDesc           SnmpAdminString,
          lldpRemSysName            SnmpAdminString,
          lldpRemSysDesc            SnmpAdminString,
          lldpRemSysCapSupported    LldpSystemCapabilitiesMap,
          lldpRemSysCapEnabled      LldpSystemCapabilitiesMap
    }
    """
    lldp_updater = _lldp_updater
    if_range = lldp_updater.oid_name_map.keys()

    lldpRemTimeMark = \
        ContextualMIBEntry('1.1', if_range, ValueType.TIME_TICKS, lldp_updater.lldp_table_lookup_integer,
                           LLDPRemoteTables(1))

    # TODO: Impl.
    # lldpRemLocalPortNum = \
    #     ContextualMIBEntry('1.2', if_range, ValueType.INTEGER, lldp_updater.lldp_subtype_id,
    #                        LLDPRemoteTables(2))
    # TODO: Impl.
    # lldpRemIndex = \
    #     ContextualMIBEntry('1.3', if_range, ValueType.INTEGER, lldp_updater.lldp_subtype_id,
    #                        LLDPRemoteTables(3))

    lldpRemChassisIdSubtype = \
        ContextualMIBEntry('1.4', if_range, ValueType.INTEGER, lldp_updater.lldp_table_lookup_integer,
                           LLDPRemoteTables(4))

    lldpRemChassisId = \
        ContextualMIBEntry('1.5', if_range, ValueType.OCTET_STRING, lldp_updater.lldp_table_lookup,
                           LLDPRemoteTables(5))

    lldpRemPortIdSubtype = \
        ContextualMIBEntry('1.6', if_range, ValueType.INTEGER, lldp_updater.lldp_table_lookup_integer,
                           LLDPRemoteTables(6))

    lldpRemPortId = \
        ContextualMIBEntry('1.7', if_range, ValueType.OCTET_STRING, lldp_updater.lldp_table_lookup,
                           LLDPRemoteTables(7))

    lldpRemPortDesc = \
        ContextualMIBEntry('1.8', if_range, ValueType.OCTET_STRING, lldp_updater.lldp_table_lookup,
                           LLDPRemoteTables(8))

    lldpRemSysName = \
        ContextualMIBEntry('1.9', if_range, ValueType.OCTET_STRING, lldp_updater.lldp_table_lookup,
                           LLDPRemoteTables(9))

    lldpRemSysDesc = \
        ContextualMIBEntry('1.10', if_range, ValueType.OCTET_STRING, lldp_updater.lldp_table_lookup,
                           LLDPRemoteTables(10))

    # TODO: Impl.
    # lldpRemSysCapSupported = \
    #     ContextualMIBEntry('1.11', if_range, ValueType.INTEGER, lldp_updater.lldp_subtype_id,
    #                        LLDPRemoteTables(11))
    # TODO: Impl.
    # lldpRemSysCapEnabled = \
    #     ContextualMIBEntry('1.12', if_range, ValueType.INTEGER, lldp_updater.lldp_subtype_id,
    #                        LLDPRemoteTables(12))
