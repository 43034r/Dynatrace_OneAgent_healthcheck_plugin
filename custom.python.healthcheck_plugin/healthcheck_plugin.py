import os, re, sys
from ruxit.api.base_plugin import BasePlugin
from ruxit.api.selectors import HostSelector
from ruxit.api.exceptions import AuthException, ConfigException
#from subprocess import check_output
import subprocess
import logging
import time



class hostHealthCheckPlugin(BasePlugin):
    def query(self, **kwargs):
        
        host_id =  self.query_snapshot.host_id
        ts_time= str(self.config["mode"])
        val_to_ctl= str(self.config["path_to_oneagentctl"])
        val_to_log= str(self.config["path_to_log"])
        if (sys.platform.startswith("win")): return
        elif (sys.platform.startswith("linux")):
            t = time.localtime()
            current_minute = time.strftime("%M", t)
            if ts_time == "1": current_minute = "00"
            if os.path.isfile(val_to_log) == False: current_minute = "00"
            if current_minute == "00" or current_minute == "15" or current_minute == "30" or current_minute == "45":
                try:
                    os.chdir("/lib64/")
                    popen_cmd=val_to_ctl +' --internal-invoked-by-installer --healthcheck | tee ' + val_to_log
                    process = subprocess.Popen(popen_cmd , stdout=subprocess.PIPE, stderr=subprocess. STDOUT, shell=True)
                    result, err = process.communicate()
                    resultdecoded = result.decode(encoding='utf-8')

                    test_name_list = re.findall(r'\[Test Name\]: (.*)', resultdecoded)
                    status_list = re.findall(r'\[Status\]: (.*)', resultdecoded)
                    success_list = re.findall(r'SUCCESS', resultdecoded)
                    failure_list = re.findall(r'FAILED', resultdecoded)
                    result_healthcheck = re.findall(r'\[Healthcheck Status\]: (.*)', resultdecoded)
                    if result_healthcheck[0]:
                        if result_healthcheck[0] == "SUCCESS":
                            self.results_builder.state_metric("oneagent_state", "OK", entity_id=host_id)
                        else:
                            self.results_builder.state_metric("oneagent_state", "Unkown", entity_id=host_id)
                    else:
                        self.results_builder.state_metric("oneagent_state", "Unkown", entity_id=host_id)
                except subprocess.CalledProcessError as grepexc:
                        if grepexc.returncode == "1":
                            self.results_builder.state_metric("oneagent_state", "Unkown", entity_id=host_id)
                        else:
                            self.results_builder.state_metric("oneagent_state", "Unkown", entity_id=host_id)

            else:
                try:
                    healthcheckfile = open(val_to_log, "r")
                    resultfromfile = healthcheckfile.read()
                    healthcheckfile.close()
                    test_name_list = re.findall(r'\[Test Name\]: (.*)', resultfromfile)
                    status_list = re.findall(r'\[Status\]: (.*)', resultfromfile)
                    result_healthcheck = re.findall(r'\[Healthcheck Status\]: (.*)', resultfromfile)
                    if result_healthcheck[0] == "SUCCESS":
                        self.results_builder.absolute(key="healthcounter",value="1",entity_id=host_id)
                        self.results_builder.state_metric("oneagent_state", "OK", entity_id=host_id)
                    elif result_healthcheck[0] == "FAILURE":
                        i=0
                        err_status_list= [ "FAILURE_user_and_group", "FAILURE_file_structure", "FAILURE_file_capabilities", "FAILURE_file_checksum", "FAILURE_selinux", "FAILURE_apparmor", "FAILURE_installer_logs", "FAILURE_watchdog_logs"]                                    
                        for element in status_list:
                            if status_list[i] == "FAILED":
                                self.results_builder.state_metric("oneagent_state", err_status_list[i], entity_id=host_id)
                            i+=1               
                    else:
                        self.logger.info( "hostHealthCheckPlugin - try to find failed stats")
                except:
                    self.results_builder.state_metric("oneagent_state", "Unkown", entity_id=host_id)