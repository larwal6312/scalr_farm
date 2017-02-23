#!/usr/bin/python
import sys
import json
import os

### Function to check python version

def checkInstallation(rv):
    currentVersion = sys.version_info
    if currentVersion[0] == rv[0] and currentVersion[1] >= rv[1]:
        pass
    else:
        sys.stderr.write( "[%s] - Error: Your Python interpreter must be %d.%d or greater (within major version %d)\n" % (sys.argv[0], rv[0], rv[1], rv[0]) )
        sys.exit(-1)
    return 0

### Check if Scalr-ctl is installed

if os.path.isfile('/usr/local/bin/scalr-ctl'):
    pass
else:
    print "You must installl scalr-ctl"
    print "To install run sudo pip install scalr-ctl"
    print "When installed you must run scalr-clt configure"
    print "You can go to http://bit.ly/2lP8ltr for a configuration guide"
    sys.exit(-1)

### Calling the 'checkInstallation' function checks if Python is >= 2.7 and < 3

requiredVersion = (2,7)
checkInstallation( requiredVersion )

### Gather some basic variables 

teamId = 38
AppOps_projectId = "9ada95ef-58ae-4e8e-955c-f0bb65859db8"
LDSN_projectId = "8f175fe2-e7b3-46d1-ba64-24b93673893f"
farmName = raw_input("what is the farm name? ")
siteName = raw_input("What is the site name? ")
owner = raw_input("Is the project owner AppOps or LDSN? ")
newsite = raw_input("Is this and existing wordpress site? Enter Y/n: ")
sitedescription = farmName
sand_subnet = "subnet-809002f7"
prod_subnet = "subnet-e806b5b1"
public_subnet = "subnet-24e5507d"
print "What size instance for the database server?"
db_size = raw_input("1) small; 2) medium: ")
print "What size instance for the web server?"
ws_size = raw_input("1) small; 2) medium: ")
print "Will the site be in production or the sandbox?"
production = raw_input("1) production; 2) sandbox: ")

if production == '1':
	print "Make sure your scalr-ctl config is set to use the production environment ID 3"
else:
	print "Make sure your scalr-ctl config is set to use the sandbox environment ID 6"

config_exit = raw_input("If config is not setup correctly press Q to exit." +
	" Otherwise press any other key to continue")

if config_exit in ('Q', 'q'):
	sys.exit("Exiting Program")

###Conditional Variables

if owner in ('LDSN', 'ldsn'):
    projectId = LDSN_projectId
else:
    projectId = AppOps_projectId

if newsite in ('Y', 'y'):
    dbname = raw_input("What is the db name? ")
    dbprefix = raw_input("what is the db prefix? ")

if db_size == '1':
    instance_dbsize = "t2.small"
else:
    instance_dbsize = "t2.medium"

if ws_size == '1':
    instance_wssize = "t2.small"
else:
    instance_wssize = "t2.medium"

if production == '2':
	subnet = sand_subnet
else:
	subnet = prod_subnet

if production == '1':
	print "Will you need a public IP?"
	public = raw_input("Press 1 for public, 0 for internal ")
	if (production == '1' and public == '1'):
		lb_subnet = public_subnet
	else:
		lb_subnet = prod_subnet
else:
	lb_subnet = sand_subnet
	public = 0

### Create farm info json

print "Creating Farm"

farm_json = {
	"description": sitedescription,
 	"teams": [
 		{
 			"id": teamId
 		},
 		{
 			"id": 29
 		},
 		{
 			"id": 34
 		}
	],
 	"project": {
 		"id": projectId
 	},
 	"timezone": "America/New_York",
 	"launchOrder": "sequential",
 	"name": farmName
 }

makeFarm = json.dumps(farm_json)
with open ('farm_info.json', 'w') as f:
	f.write(makeFarm)

### Send command to scalr to create farm

os.system("scalr-ctl farms create  --stdin < farm_info.json")

### Get Farm ID 

farmID = raw_input("Input farm ID from output." +
	" It is listed under description: ")

### Create json files for farm global variables

if public == '1':
	public_json = {
		"value": 1
	}
	public_update = json.dumps(public_json)
	with open ('public_update.json') as f:
		f.write(public_update)
	os.system("scalr-ctl farm-global-variables create --farmId " + farmID + " --stdin < masterIP.json > /dev/null")

masterip_json = {
	"category": "",
	"description": "",
	"hidden": 0,
	"locked": 0,
	"name": "MASTER_IP",
	"outputFormat": "",
	"requiredIn": "",
	"validationPattern": "",
	"value": ""
}
masterip = json.dumps(masterip_json)
with open ('masterIP.json', 'w') as f:
	f.write(masterip)

mysqlrole_json = {
		"category": "",
	"description": "",
	"hidden": 0,
	"locked": 0,
	"name": "MYSQL_ROLE",
	"outputFormat": "",
	"requiredIn": "",
	"validationPattern": "",
	"value": "master"
}

mysqlrole = json.dumps(mysqlrole_json)
with open ('mysqlrole.json', 'w') as f:
	f.write(mysqlrole)

sitename_json = {
	"category": "",
	"description": "",
	"hidden": 0,
	"locked": 0,
	"name": "WP_SITENAME",
	"outputFormat": "",
	"requiredIn": "",
	"validationPattern": "",
	"value": siteName
}

sitename = json.dumps(sitename_json)
with open ('sitename.json', 'w') as f:
	f.write(sitename)

if newsite in ('Y', 'y'):
	DBname_json = {
		"category": "",
		"description": "",
		"hidden": 0,
		"locked": 0,
		"name": "WP_DB",
		"outputFormat": "",
		"requiredIn": "",
		"validationPattern": "",
		"value": dbname
	}

	DBname = json.dumps(DBname_json)
	with open ('DBname.json', 'w') as f:
		f.write(DBname)

	DBprefix_json = {
		"category": "",
		"description": "",
		"hidden": 0,
		"locked": 0,
		"name": "WP_PREFIX",
		"outputFormat": "",
		"requiredIn": "",
		"validationPattern": "",
		"value": dbprefix
	}

	DBprefix = json.dumps(DBprefix_json)
	with open ('DBprefix.json', 'w') as f:
		f.write(DBprefix)


### Send command to scalr for global variable

os.system("scalr-ctl farm-global-variables create --farmId " + farmID + " --stdin < masterIP.json > /dev/null")
os.system("scalr-ctl farm-global-variables create --farmId " + farmID + " --stdin < mysqlrole.json > /dev/null")
os.system("scalr-ctl farm-global-variables create --farmId " + farmID + " --stdin < sitename.json > /dev/null")

if newsite in ('Y', 'y'):
	os.system("scalr-ctl farm-global-variables create --farmId " + farmID + " --stdin < DBname.json > /dev/null")
	os.system("scalr-ctl farm-global-variables create --farmId " + farmID + " --stdin < DBprefix.json > /dev/null")

### Create Farm role json's for lb

print "Creating LB role"

lbrole_json = {
	"alias": "lb-" + farmName,
	"instance": {
		"instanceConfigurationType": "AwsInstanceConfiguration",
		"instanceType": {
			"id": "t2.micro"
		}
	},
	"placement": {
		"placementConfigurationType": "AwsVpcPlacementConfiguration",
		"region": "us-east-1",
		"vpc": {
			"id": "vpc-54d5bb31"
		},
		"subnets": [{
			"id": lb_subnet
		}]
	},
	"platform": "ec2",
	"role": {
		"id": 79176
	},
	"scaling": {
		"considerSuspendedServers": "running",
		"enabled": 1,
		"maxInstances": 1,
		"minInstances": 1,
		"scalingBehavior": "launch-terminate"
	}
}

lbfarmrole = json.dumps(lbrole_json)
with open ('lbfarmrole.json', 'w') as f:
	f.write(lbfarmrole)

### Send command to scalr to create lb role and collect role ID

os.system("scalr-ctl farm-roles create --farmId " + farmID + " --stdin < lbfarmrole.json")

lbroleID = raw_input("Input farm role ID from output." +
	" It is listed under farm ID: ")

### Create Farm role json's for db

print "Creating DB role"

dbrole_json = {
	"alias": "db-" + farmName,
	"instance": {
		"instanceConfigurationType": "AwsInstanceConfiguration",
		"instanceType": {
			"id": instance_dbsize
		}
	},
	"placement": {
		"placementConfigurationType": "AwsVpcPlacementConfiguration",
		"region": "us-east-1",
		"vpc": {
			"id": "vpc-54d5bb31"
		},
		"subnets": [{
			"id": subnet
		}]
	},
	"platform": "ec2",
	"role": {
		"id": 79176
	},
	"scaling": {
		"considerSuspendedServers": "running",
		"enabled": 1,
		"maxInstances": 1,
		"minInstances": 1,
		"scalingBehavior": "launch-terminate"
	}
} 

dbfarmrole = json.dumps(dbrole_json)
with open ('dbfarmrole.json', 'w') as f:
	f.write(dbfarmrole)

### Send command to scalr to create db role and collect role ID

os.system("scalr-ctl farm-roles create --farmId " + farmID + " --stdin < dbfarmrole.json")

dbroleID = raw_input("Input farm role ID from output." +
	" It is listed under farm ID: ")

### Create Farm role json's for ws

print "Creating WS role"

wsrole_json = {
	"alias": "web-" + farmName,
	"instance": {
		"instanceConfigurationType": "AwsInstanceConfiguration",
		"instanceType": {
			"id": instance_wssize
		}
	},
	"placement": {
		"placementConfigurationType": "AwsVpcPlacementConfiguration",
		"region": "us-east-1",
		"vpc": {
			"id": "vpc-54d5bb31"
		},
		"subnets": [{
			"id": subnet
		}]
	},
	"platform": "ec2",
	"role": {
		"id": 79122
	},
	"scaling": {
		"considerSuspendedServers": "running",
		"enabled": 1,
		"maxInstances": 1,
		"minInstances": 1,
		"scalingBehavior": "launch-terminate"
	}
}

wsfarmrole = json.dumps(wsrole_json)
with open ('wsfarmrole.json', 'w') as f:
	f.write(wsfarmrole)

### Send command to scalr to create ws role and collect role ID

os.system("scalr-ctl farm-roles create --farmId " + farmID + " --stdin < wsfarmrole.json")

wsroleID = raw_input("Input farm role ID from output." +
	" It is listed under farm ID: ")

### Create json files for lb global variables 

print "Creating global variables for LB"

lbDNS_json = {
	"category": "",
	"description": "",
	"hidden": 0,
	"locked": 0,
	"name": "DNS",
	"outputFormat": "",
	"requiredIn": "",
	"validationPattern": "",
	 "value": ""
}

lbDNS = json.dumps(lbDNS_json)
with open ('lbDNS.json', 'w') as f:
	f.write(lbDNS)

lbHAPROXY_json = {
	"category": "",
	"description": "",
	"hidden": 0,
	"locked": 0,
	"name": "HAPROXY_CONFIGURATION",
	"outputFormat": "",
	"requiredIn": "",
	"validationPattern": "",
	"value": "[\n{\n   \"name\": \"unsecure\",\n   \"listen\": {\n     \"bind\": \"*\",\n     \"port\": 80\n   },\n   \"upstream\": {\n     \"alias\": \"web-%s\",\n     \"port\": 80\n   }\n}\n]" % (farmName)
}

lbHAPROXY = json.dumps(lbHAPROXY_json)
with open ('lbHAPROXY.json', 'w') as f:
	f.write(lbHAPROXY)

### Send command to scalr to create lb global variables

os.system("scalr-ctl farm-role-global-variables create --farmRoleId " + lbroleID + " --stdin < lbDNS.json > /dev/null")
os.system("scalr-ctl farm-role-global-variables create --farmRoleId " + lbroleID + " --stdin < lbHAPROXY.json > /dev/null")

### Create json files for lb orchestration

print "Creating orchestraton scripts for LB"

lbDNSipchange_json = {
	"action": {
		"actionType": "ScriptAction",
		"scriptVersion": {
			"script": {
				"id": 264
			},
			"version": -1
		}
	},
	"blocking": 1,
	"order": 10,
	"runAs": "",
	"target": {
		"targetType": "TriggeringServerTarget"
	},
	"timeout": 180,
	"trigger": {
		"triggerType": "SpecificEventTrigger",
		"event": {
			"id": "IPAddressChanged"
		}
	}
}

lbDNSipchange = json.dumps(lbDNSipchange_json)
with open ('lbDNSipchange.json', 'w') as f:
	f.write(lbDNSipchange)

lbHAhostup_json = {
	"action": {
		"actionType": "ScriptAction",
		"scriptVersion": {
			"script": {
				"id": 266
			},
			"version": -1
		}
	},
	"blocking": 1,
	"order": 7,
	"runAs": "",
	"target": {
		"targetType": "TriggeringServerTarget"
	},
	"timeout": 180,
	"trigger": {
		"triggerType": "SpecificEventTrigger",
		"event": {
			"id": "HostUp"
		}
	}
}

lbHAhostup = json.dumps(lbHAhostup_json)
with open ('lbHAhostup.json', 'w') as f:
	f.write(lbHAhostup)

AWSCLIhostup_json = {
	"action": {
		"actionType": "ScriptAction",
		"scriptVersion": {
			"script": {
				"id": 265
			},
			"version": -1
		}
	},
	"blocking": 1,
	"order": 8,
	"runAs": "",
	"target": {
		"targetType": "TriggeringServerTarget"
	},
	"timeout": 180,
	"trigger": {
		"triggerType": "SpecificEventTrigger",
		"event": {
			"id": "HostUp"
		}
	}
}

AWSCLIhostup = json.dumps(AWSCLIhostup_json)
with open ('AWSCLIhostup.json', 'w') as f:
	f.write(AWSCLIhostup)

lbDNShostup_json = {
	"action": {
		"actionType": "ScriptAction",
		"scriptVersion": {
			"script": {
				"id": 264
			},
			"version": -1
		}
	},
	"blocking": 1,
	"order": 9,
	"runAs": "",
	"target": {
		"targetType": "TriggeringServerTarget"
	},
	"timeout": 180,
	"trigger": {
		"triggerType": "SpecificEventTrigger",
		"event": {
			"id": "HostUp"
		}
	}
}

lbDNShostup = json.dumps(lbDNShostup_json)
with open ('lbDNShostup.json', 'w') as f:
	f.write(lbDNShostup)

lbDNShostdown_json = {
	"action": {
		"actionType": "ScriptAction",
		"scriptVersion": {
			"script": {
				"id": 264
			},
			"version": -1
		}
	},
	"blocking": 1,
	"order": 10,
	"runAs": "",
	"target": {
		"targetType": "NullTarget"
	},
	"timeout": 180,
	"trigger": {
		"triggerType": "SpecificEventTrigger",
		"event": {
			"id": "HostDown"
		}
	}
}

lbDNShostdown = json.dumps(lbDNShostdown_json)
with open ('lbDNShostdown.json', 'w') as f:
	f.write(lbDNShostdown)

### Send command to scalr to create orchestration scripts

os.system("scalr-ctl farm-role-orchestration-rules create --farmRoleId " + lbroleID + " --stdin < lbDNSipchange.json > /dev/null")
os.system("scalr-ctl farm-role-orchestration-rules create --farmRoleId " + lbroleID + " --stdin < lbHAhostup.json > /dev/null")
os.system("scalr-ctl farm-role-orchestration-rules create --farmRoleId " + lbroleID + " --stdin < AWSCLIhostup.json > /dev/null")
os.system("scalr-ctl farm-role-orchestration-rules create --farmRoleId " + lbroleID + " --stdin < lbDNShostup.json > /dev/null")
os.system("scalr-ctl farm-role-orchestration-rules create --farmRoleId " + lbroleID + " --stdin < lbDNShostdown.json > /dev/null")

### Create json files for db orchestration

print "Creating global variables for DB"

dbMYSQLmasterIP_json = {
	"action": {
		"actionType": "ScriptAction",
		"scriptVersion": {
			"script": {
				"id": 197
			},
			"version": -1
		}
	},
	"blocking": 1,
	"order": 10,
	"runAs": "",
	"target": {
		"targetType": "TriggeringServerTarget"
	},
	"timeout": 180,
	"trigger": {
		"triggerType": "SpecificEventTrigger",
		"event": {
			"id": "HostUp"
		}
	}
}

dbMYQSLmasterIP = json.dumps(dbMYSQLmasterIP_json)
with open ('dbMYSQLmasterIP.json', 'w') as f:
	f.write(dbMYQSLmasterIP)

### Send command to scalr to create orchestration scripts

os.system("scalr-ctl farm-role-orchestration-rules create --farmRoleId " + dbroleID + " --stdin < dbMYSLmasterIP.json > /dev/null")

### Create json files for ws orchestration

print "Creating orchestration scripts for WS"

wsHAPROXYhostup_json = {
  "action": {
    "actionType": "ScriptAction",
    "scriptVersion": {
      "script": {
        "id": 266
      },
      "version": -1
    }
  },
  "blocking": 1,
  "order": 10,
  "runAs": "",
  "target": {
    "targetType": "SelectedFarmRolesTarget",
    "roles": [
      {
        "id": lbroleID
      }
    ]
  },
  "timeout": 180,
  "trigger": {
    "triggerType": "SpecificEventTrigger",
    "event": {
      "id": "HostUp"
    }
  }
}

wsHAPROXYhostup = json.dumps(wsHAPROXYhostup_json)
with open ('wsHAPROXYhostup.json', 'w') as f:
	f.write(wsHAPROXYhostup)

wsHAPROXYhostdown_json = {
  "action": {
    "actionType": "ScriptAction",
    "scriptVersion": {
      "script": {
        "id": 266
      },
      "version": -1
    }
  },
  "blocking": 1,
  "order": 10,
  "runAs": "",
  "target": {
    "targetType": "SelectedFarmRolesTarget",
    "roles": [
      {
        "id": lbroleID
      }
    ]
  },
  "timeout": 180,
  "trigger": {
    "triggerType": "SpecificEventTrigger",
    "event": {
      "id": "HostDown"
    }
  }
}

wsHAPROXYhostdown = json.dumps(wsHAPROXYhostdown_json)
with open ('wsHAPROXYhostdown.json', 'w') as f:
	f.write(wsHAPROXYhostdown)

### Send command to scalr to create orchestration scripts

os.system("scalr-ctl farm-role-orchestration-rules create --farmRoleId " + wsroleID + " --stdin < wsHAPROXYhostup.json > /dev/null")
os.system("scalr-ctl farm-role-orchestration-rules create --farmRoleId " + wsroleID + " --stdin < wsHAPROXYhostdown.json > /dev/null")

### EOF
print "Your farm has been created. Buh-bye!"
