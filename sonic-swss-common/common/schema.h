#ifndef __SCHEMA__
#define __SCHEMA__

namespace swss {

/***** DATABASE *****/

#define APPL_DB         0
#define ASIC_DB         1
#define COUNTERS_DB     2
#define LOGLEVEL_DB     3
#define CONFIG_DB       4
#define PFC_WD_DB       5
#define STATE_DB        6

/***** APPLICATION DATABASE *****/

#define APP_PORT_TABLE_NAME             "PORT_TABLE"
#define APP_VLAN_TABLE_NAME             "VLAN_TABLE"
#define APP_VLAN_MEMBER_TABLE_NAME      "VLAN_MEMBER_TABLE"
#define APP_LAG_TABLE_NAME              "LAG_TABLE"
#define APP_LAG_MEMBER_TABLE_NAME       "LAG_MEMBER_TABLE"
#define APP_INTF_TABLE_NAME             "INTF_TABLE"
#define APP_NEIGH_TABLE_NAME            "NEIGH_TABLE"
#define APP_ROUTE_TABLE_NAME            "ROUTE_TABLE"
#define APP_TUNNEL_DECAP_TABLE_NAME     "TUNNEL_DECAP_TABLE"
#define APP_MIRROR_SESSION_TABLE_NAME   "MIRROR_SESSION_TABLE"
#define APP_ACL_TABLE_NAME              "ACL_TABLE"
#define APP_ACL_RULE_TABLE_NAME         "ACL_RULE_TABLE"
#define APP_FDB_TABLE_NAME              "FDB_TABLE"
#define APP_PFC_WD_TABLE_NAME           "PFC_WD_TABLE"
#define APP_SWITCH_TABLE_NAME           "SWITCH_TABLE"

#define APP_TC_TO_QUEUE_MAP_TABLE_NAME  "TC_TO_QUEUE_MAP_TABLE"
#define APP_SCHEDULER_TABLE_NAME        "SCHEDULER_TABLE"
#define APP_DSCP_TO_TC_MAP_TABLE_NAME   "DSCP_TO_TC_MAP_TABLE"
#define APP_QUEUE_TABLE_NAME            "QUEUE_TABLE"
#define APP_PORT_QOS_MAP_TABLE_NAME     "PORT_QOS_MAP_TABLE"
#define APP_WRED_PROFILE_TABLE_NAME     "WRED_PROFILE_TABLE"
#define APP_BUFFER_POOL_TABLE_NAME      "BUFFER_POOL_TABLE"
#define APP_BUFFER_PROFILE_TABLE_NAME   "BUFFER_PROFILE_TABLE"
#define APP_BUFFER_QUEUE_TABLE_NAME     "BUFFER_QUEUE_TABLE"
#define APP_BUFFER_PG_TABLE_NAME        "BUFFER_PG_TABLE"
#define APP_BUFFER_PORT_INGRESS_PROFILE_LIST_NAME   "BUFFER_PORT_INGRESS_PROFILE_LIST"
#define APP_BUFFER_PORT_EGRESS_PROFILE_LIST_NAME    "BUFFER_PORT_EGRESS_PROFILE_LIST"
#define APP_COPP_TABLE_NAME                         "COPP_TABLE"
#define APP_TC_TO_PRIORITY_GROUP_MAP_NAME           "TC_TO_PRIORITY_GROUP_MAP_TABLE"
#define APP_PFC_PRIORITY_TO_PRIORITY_GROUP_MAP_NAME "PFC_PRIORITY_TO_PRIORITY_GROUP_MAP_TABLE"
#define APP_PFC_PRIORITY_TO_QUEUE_MAP_NAME          "MAP_PFC_PRIORITY_TO_QUEUE"

/***** COUNTER DATABASE *****/

#define COUNTERS_PORT_NAME_MAP          "COUNTERS_PORT_NAME_MAP"
#define COUNTERS_TABLE                  "COUNTERS"
#define COUNTERS_QUEUE_NAME_MAP         "COUNTERS_QUEUE_NAME_MAP"
#define COUNTERS_QUEUE_PORT_MAP         "COUNTERS_QUEUE_PORT_MAP"
#define COUNTERS_QUEUE_INDEX_MAP        "COUNTERS_QUEUE_INDEX_MAP"

#define DAEMON_TABLE_NAME "DAEMON_TABLE"
#define DAEMON_LOGLEVEL "LOGLEVEL"

/***** PFC WATCHDOG DATABASE *****/

#define PFC_WD_STATE_TABLE "PFC_WD_STATE_TABLE"
#define PFC_WD_PORT_COUNTER_ID_LIST "PORT_COUNTER_ID_LIST"
#define PFC_WD_QUEUE_COUNTER_ID_LIST "QUEUE_COUNTER_ID_LIST"
#define PFC_WD_QUEUE_ATTR_ID_LIST "QUEUE_ATTR_ID_LIST" 
#define PLUGIN_TABLE "PLUGIN_TABLE"
#define SAI_OBJECT_TYPE "SAI_OBJECT_TYPE"

/***** STATE DATABASE *****/

#define STATE_PORT_TABLE_NAME           "PORT_TABLE"
#define STATE_INTERFACE_TABLE_NAME      "INTERFACE_TABLE"

/***** MISC *****/

#define IPV4_NAME "IPv4"
#define IPV6_NAME "IPv6"

#define SET_COMMAND "SET"
#define DEL_COMMAND "DEL"
#define EMPTY_PREFIX ""

}

#endif
