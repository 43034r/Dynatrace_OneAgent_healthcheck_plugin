# Dynatrace_OneAgent_healthcheck_plugin

Description:
Plugin uses oneagentctl healthcheck command.
2 Modes avaliable: every 15 minutes(00, 15, 30, 45) and every minute.
Plugin uses status metrics. Consumes only one metric. 
Host level view:
![image](https://github.com/43034r/Dynatrace_OneAgent_healthcheck_plugin/assets/91538748/ea5e4006-cb20-4db5-a844-e86c7e6470c4)

Problem example:
![image](https://github.com/43034r/Dynatrace_OneAgent_healthcheck_plugin/assets/91538748/530171e5-1188-4f33-93ec-a737e0cc2212)

Settings:
You need to provide path to oneagentctl and path to log folder including filename.
![image](https://github.com/43034r/Dynatrace_OneAgent_healthcheck_plugin/assets/91538748/25c95138-948b-46c2-afc4-ca15f051fb29)

default path to oneagentctl:
**/opt/dynatrace/oneagent/agent/tools/oneagentctl**

default path to logs: /var/log/dynatrace/oneagent/

recommended path to healthcheck file:
**/var/log/dynatrace/oneagent/healthcheck**

mode - 0 - execution in minutes (00, 15, 30, 45)
mode - 1 - execution every minute

Detects:

FAILURE_user_and_group

FAILURE_file_structure

FAILURE_file_capabilities

FAILURE_file_checksum

FAILURE_selinux

FAILURE_apparmor

FAILURE_installer_logs

FAILURE_watchdog_logs

Plugin works only on linux.


