#/bin/bash
##########################################################
#
#   DBLINK
#
##########################################################

# 1./opt/192.168.31.31/gcluster/config/gbase_8a_gcluster.cnf
[root@localhost config]# cat /opt/192.168.31.31/gcluster/config/gbase_8a_gcluster.cnf
# 添加如下参数
gbase_dblink_gateway_ip = 192.168.31.31
gbase_dblink_gateway_port = 9898

gcluster_services all restart

# 2.解压压缩包

# 3./opt/gbase_workspace/setup/Gateway_8.5.1.2_build4.28/conf/conf.properties
# 默认即可

# 4./opt/gbase_workspace/setup/Gateway_8.5.1.2_build4.28/conf/gcluster/gbase8a_gcluster.properties
[root@localhost conf]# cat gcluster/gbase8a_gcluster.properties
[gc1]
gcluster_IP=192.168.31.31
gcluster_port=5258
gcluster_user=gbase
gcluster_pwd=X@gbase2018
gcluster_encode=utf8mb4
[gc2]
...
[gn1]
gcluster_IP=192.168.31.32
gcluster_port=5050
gcluster_user=gbase
gcluster_pwd=X@gbase2018
gcluster_encode=utf8mb4
[gn2]
...

# 5./opt/gbase_workspace/setup/Gateway_8.5.1.2_build4.28/conf/dataSource/mysql_dblink1.properties
[root@localhost dataSource]# cat mysql_dblink1.properties
[ds1]
dataSource_dbtype=mysql
dataSource_url=jdbc:mysql://192.168.31.136:3306/mydb
dataSource_IP=192.168.31.136
dataSource_port=3306
dataSource_dbname=mydb
dataSource_user=zhanghe
dataSource_pwd=123456

CREATE DATABASE LINK dblink_name CONNECT TO username IDENTIFIED BY password USING  gc_link ';


##########################################################
#
#   AKshare数据整合
#
##########################################################
cd /home/king/python/Trading/akshare_file_data/datafile

cat 01stock_individual_info.txt >               /home/king/stock_individual_info.txt
cat 02stock_zh_a_spot.txt >                     /home/king/stock_zh_a_spot.txt
cat 03stock_zh_a_hist*.txt >                    /home/king/stock_zh_a_hist.txt
cat 04stock_news*.txt >                         /home/king/stock_news.txt
cat 05stock_yjbb*.txt >                         /home/king/stock_yjbb.txt
cat 06stock_profit_forecast.txt >               /home/king/stock_profit_forecast.txt
cat 07stock_board_industry_summary_ths.txt >    /home/king/stock_board_industry_summary_ths.txt


##########################################################
#
#   Gase物理空间
#
##########################################################
[root@localhost sys_tablespace]# du -sh /opt/192.168.*/gnode/userdata/gbase/mydb/sys_tablespace/stock_news2*
64M     /opt/192.168.31.32/gnode/userdata/gbase/mydb/sys_tablespace/stock_news2_n1
69M     /opt/192.168.31.33/gnode/userdata/gbase/mydb/sys_tablespace/stock_news2_n2
76M     /opt/192.168.31.34/gnode/userdata/gbase/mydb/sys_tablespace/stock_news2_n3
138M    /opt/192.168.31.35/gnode/userdata/gbase/mydb/sys_tablespace/stock_news2_n4


##########################################################
#
#   数据倾斜（数据节点数据量）和空洞（MAX(rowid)
#
##########################################################
gccli -ugbase -p123456 -h192.168.31.32 -P5050 -Ns -e"select count(1) from mydb.stock_news2_n1"
gccli -ugbase -p123456 -h192.168.31.33 -P5050 -Ns -e"select count(1) from mydb.stock_news2_n2"
gccli -ugbase -p123456 -h192.168.31.34 -P5050 -Ns -e"select count(1) from mydb.stock_news2_n3"
gccli -ugbase -p123456 -h192.168.31.35 -P5050 -Ns -e"select count(1) from mydb.stock_news2_n4"

gccli -ugbase -p123456 -h192.168.31.32 -P5050 -Ns -e "select count(1),nvl(max(rowid)+1,0) from mydb.stock_news2_n1"
gccli -ugbase -p123456 -h192.168.31.33 -P5050 -Ns -e "select count(1),nvl(max(rowid)+1,0) from mydb.stock_news2_n2"
gccli -ugbase -p123456 -h192.168.31.34 -P5050 -Ns -e "select count(1),nvl(max(rowid)+1,0) from mydb.stock_news2_n3"
gccli -ugbase -p123456 -h192.168.31.35 -P5050 -Ns -e "select count(1),nvl(max(rowid)+1,0) from mydb.stock_news2_n4"