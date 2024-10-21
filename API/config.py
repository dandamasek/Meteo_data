#CONFIG_FILE

# CLIMATE_DATA = "meteorology/climate/now/data/10m-0-20000-0-11683-20241002.json"
# CLIMATE_METADATA = "meteorology/climate/now/metadata/meta1-20240930.json"
# WEATHER_ALERTS = "meteorology/weather/alerts/cap/alert_cap_010823.xml"
# WEATHER_RADAR_COMPOSITE_ECHOTOP = "meteorology/weather/radar/composite/echotop/hdf5/T_PADV23_C_OKPR_20240925150500.hdf"
# WEATHER_NWP_ALADIN = "meteorology/weather/nwp_aladin/CZ_1km/00/ALADCZ1K4opendata_2024100200_SURFPREC_TOTAL.grb.bz2"

BUCKETNAME = "meteodatabucket"

DOMAINLA = "https://opendata.chmi.cz/meteorology/weather/nwp_aladin/Lambert_2.3km/00/ALADLAMB4opendata_"

DOMAINCZ = "https://opendata.chmi.cz/meteorology/weather/nwp_aladin/CZ_1km/"
SUBDOMAINCZ = "/ALADCZ1K4opendata_"

ALADIN_ATTRIBUTES = {
"MSLPRESSURE" : "MSLPRESSURE",
"CLSTEMPERATURE" : "CLSTEMPERATURE", 
"CLSHUMI_RELATIVE" : "CLSHUMI_RELATIVE",
"CLSWIND_SPEED" : "CLSWIND_SPEED",
"CLSWIND_DIREC" : "CLSWIND_DIREC",           # not in CZ1
"CLSU_RAF_MOD_XFU" : "CLSU_RAF_MOD_XFU",
"CLSV_RAF_MOD_XFU" : "CLSV_RAF_MOD_XFU",
"SURFNEBUL_BASSE" : "SURFNEBUL_BASSE",
"SURFNEBUL_MOYENN" : "SURFNEBUL_MOYENN",
"SURFNEBUL_HAUTE" : "SURFNEBUL_HAUTE",
"CLS_VISICLD" : "CLS_VISICLD",
"CLS_VISIPRE" : "CLS_VISIPRE",
"SURFRAINFALL" : "SURFRAINFALL",
"SURFSNOWFALL" : "SURFSNOWFALL",
"SURFPREC_TOTAL" : "SURFPREC_TOTAL",
"PRECIP_TYPE" : "PRECIP_TYPE",
"PRECIP_TYPESEV" : "PRECIP_TYPESEV",
"SURFCAPE_POS_F00" : "SURFCAPE_POS_F00",     # not in CZ1
"SURFCIEN_POS_F00" : "SURFCIEN_POS_F00",
"SURFDIAG_FLASH" : "SURFDIAG_FLASH",         # not in CZ!
"MAXSIM_REFLECTI" : "MAXSIM_REFLECTI",
"SURFNEBUL_TOTALE" : "SURFNEBUL_TOTALE",     # good-to-have
"CLPVEIND_MOD_XFU" : "CLPVEIND_MOD_XFU",     # good-to-have
"SURFRF_SHORT_DO" : "SURFRF_SHORT_DO",       # good-to-have
"SURFRF_LONG_DO" : "SURFRF_LONG_DO",         # good-to-have
"SURF_RAYT_DIR" : "SURF_RAYT_DIR",           # good-to-have
"SUNSHINE_DUR" : "SUNSHINE_DUR",             # good-to-have
"SURFRESERV_NEIGE" : "SURFRESERV_NEIGE",     # good-to-have

}