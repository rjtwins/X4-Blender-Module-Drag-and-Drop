#naming scheme
#Cotains names and associated tags
tag_dict =	{
#generic
  "generic": "",
#turrets
  "lturret": 	"turret large standard hittable",
  "lmturret": 	"turret large standard missile hittable",
  "mturret": 	"turret medium standard hittable",
  "mmturret": 	"turret medium standard missile hittable",
  "sturret": 	"turret small standard hittable",
  "ssturret": 	"turret small standard missile hittable",
#Shields
  "xlshield": 	"extralarge shield hittable",
  "lshield": 	"large shield hittable",
  "mshield": 	"medium shield hittable",
  "sshield": 	"small shield",
#Engines
  "xlengine":	"engine extralarge",
  "lengine": 	"engine large",
  "mengine": 	"engine medium",
  "sengine": 	"engine small platformcollision",
#countermeasures
  "counter":  "countermeasures",
#Fixed weapons
  "lweap" : "weapon large standard",
  "mweap" : "weapon medium standard platformcollision",
  "sweap" : "weapon small standard platformcollision",
  "lmweap" : "weapon large standard missile",
  "mmweap" : "weapon medium standard missile platformcollision",
  "smweap" : "weapon small standard missile platformcollision",
#waypoints
  "stawaypoint" : "sizeLevel1 typedock start dynamicmasstraffic",
  "endwaypoint" : "sizeLevel1 typedock end dynamicmasstraffic",
  "waypoint" : "typenormal sizeLevel1 dynamicmasstraffic",
  "clowaypoint" : "typenormal sizeLevel1 dynamicmasstraffic closelink",
#Player controll/cockpids
  "playerctrl" : "playercontrol",
  "cockpit": "cockpit cockpit_visible",
#Storage modules
  "shipstorage" : "dockingbay",
  "storage" : "storage",
#Dockging
  "dock_xs" : "dock_xs",
  "dockarea" : "dockarea"
}

name_dict = {
#Generic
  "generic" : "con_generic",
 #Turrets 
  "lturret": 	"con_l_turret",
  "lmturret": 	"con_lm_turret",
  "mturret": 	"con_m_turret",
  "mmturret": 	"con_mm_turret",
  "sturret": 	"con_s_turret",
  "smturret": 	"con_sm_turret",
#Shields
  "xlshield": 	"con_shieldgen_xl",
  "lshield": 	"con_shieldgen_l",
  "mshield": 	"con_shieldgen_m",
  "sshield": 	"con_shieldgen_s",
 #Engines
  "xlengine": 	"con_engine_xl",
  "lengine": 	"con_engine_l",
  "mengine": 	"con_engine_m",
  "sengine": 	"con_engine_s",
#Countermeasures
  "counter": "con_countermeasures",
#Fixed weapons 
  "lweap" : "con_l_yweapon",
  "mweap" : "con_m_weapon",
  "sweap" : "con_s_weapon",
  "lmweap" : "con_lm_yweapon",
  "mmweap" : "con_mm_weapon",
  "smweap" : "con_sm_weapon",
#Waypoints
  "stawaypoint" : "XU_Waypoint",
  "endwaypoint" : "XU_Waypoint",
  "waypoint" : "XU_Waypoint",
  "clowaypoint" : "XU_Waypoint",
#Player controll/cockpit
  "playerctrl" : "con_playercontrol",
  "cockpit": "con_cockpit",
#Storage modules
  "storage" : "con_storage",
  "shipstorage" : "con_shipstorage",
#Docking
  "dock_xs" : "con_dock",
  "dockarea" : "con_dockarea"
}