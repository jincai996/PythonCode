/*
	用户资源组配置
*/

USE sys_vc;

-- 创建用户
CREATE USER 'ysj_admin'@'%' IDENTIFIED BY 'Gbase2024!';
CREATE USER 'ysj_user1'@'%' IDENTIFIED BY 'Gbase2021!';
CREATE USER 'ysj_user2'@'%' IDENTIFIED BY 'Gbase2021!';
CREATE USER 'ysj_user3'@'%' IDENTIFIED BY 'Gbase2021!';
CREATE USER 'ysj_user4'@'%' IDENTIFIED BY 'Gbase2021!';
CREATE USER 'ysj_user5'@'%' IDENTIFIED BY 'Gbase2021!';
CREATE USER 'ysj_user6'@'%' IDENTIFIED BY 'Gbase2021!';
CREATE USER 'ysj_user7'@'%' IDENTIFIED BY 'Gbase2021!';
CREATE USER 'ysj_user8'@'%' IDENTIFIED BY 'Gbase2021!';
CREATE USER 'ysj_user9'@'%' IDENTIFIED BY 'Gbase2021!';
CREATE USER 'ysj_user10'@'%' IDENTIFIED BY 'Gbase2021!';

-- 创建数据库
CREATE DATABASE ysj_database1;
CREATE DATABASE ysj_database2;
CREATE DATABASE ysj_database3;
CREATE DATABASE ysj_database4;
CREATE DATABASE ysj_database5;
CREATE DATABASE ysj_database6;
CREATE DATABASE ysj_database7;
CREATE DATABASE ysj_database8;
CREATE DATABASE ysj_database9;
CREATE DATABASE ysj_database10;

-- admin用户权限
GRANT FILE ON  *.*.*           TO ysj_admin@'%';  
GRANT ALL  ON ysj_database1.*  TO ysj_admin@'%';
GRANT ALL  ON ysj_database2.*  TO ysj_admin@'%';
GRANT ALL  ON ysj_database3.*  TO ysj_admin@'%';
GRANT ALL  ON ysj_database4.*  TO ysj_admin@'%';
GRANT ALL  ON ysj_database5.*  TO ysj_admin@'%';
GRANT ALL  ON ysj_database6.*  TO ysj_admin@'%';
GRANT ALL  ON ysj_database7.*  TO ysj_admin@'%';
GRANT ALL  ON ysj_database8.*  TO ysj_admin@'%';
GRANT ALL  ON ysj_database9.*  TO ysj_admin@'%';
GRANT ALL  ON ysj_database10.* TO ysj_admin@'%';

-- ysj_user1~9用户权限
GRANT ALL  ON ysj_database1.*  TO ysj_user1@'%';
GRANT ALL  ON ysj_database2.*  TO ysj_user2@'%';
GRANT ALL  ON ysj_database3.*  TO ysj_user3@'%';
GRANT ALL  ON ysj_database4.*  TO ysj_user4@'%';
GRANT ALL  ON ysj_database5.*  TO ysj_user5@'%';
GRANT ALL  ON ysj_database6.*  TO ysj_user6@'%';
GRANT ALL  ON ysj_database7.*  TO ysj_user7@'%';
GRANT ALL  ON ysj_database8.*  TO ysj_user8@'%';
GRANT ALL  ON ysj_database9.*  TO ysj_user9@'%';
GRANT ALL  ON ysj_database10.* TO ysj_user10@'%';

-- ysj_admin ysj_user1~9默认VC
SET default_vc FOR ysj_admin = vc_competition;
SET default_vc FOR ysj_user1 = vc_competition;
SET default_vc FOR ysj_user2 = vc_competition;
SET default_vc FOR ysj_user3 = vc_competition;
SET default_vc FOR ysj_user4 = vc_competition;
SET default_vc FOR ysj_user5 = vc_competition;
SET default_vc FOR ysj_user6 = vc_competition;
SET default_vc FOR ysj_user7 = vc_competition;
SET default_vc FOR ysj_user8 = vc_competition;
SET default_vc FOR ysj_user9 = vc_competition;
SET default_vc FOR ysj_user10 = vc_competition;

######################################################################################

-- 创建用户自定义资源消费组
CREATE CONSUMER GROUP group1 COMMENT = 'group1';
CREATE CONSUMER GROUP group2 COMMENT = 'group2';
CREATE CONSUMER GROUP group3 COMMENT = 'group3';
CREATE CONSUMER GROUP group4 COMMENT = 'group4';
CREATE CONSUMER GROUP group5 COMMENT = 'group5';
CREATE CONSUMER GROUP group6 COMMENT = 'group6';
CREATE CONSUMER GROUP group7 COMMENT = 'group7';
CREATE CONSUMER GROUP group8 COMMENT = 'group8';
CREATE CONSUMER GROUP group9 COMMENT = 'group9';
CREATE CONSUMER GROUP group10 COMMENT = 'group10';

-- 将用户添加到资源消费组
ALTER CONSUMER GROUP group1 ADD USER ysj_user1;
ALTER CONSUMER GROUP group2 ADD USER ysj_user2;
ALTER CONSUMER GROUP group3 ADD USER ysj_user3;
ALTER CONSUMER GROUP group4 ADD USER ysj_user4;
ALTER CONSUMER GROUP group5 ADD USER ysj_user5;
ALTER CONSUMER GROUP group6 ADD USER ysj_user6;
ALTER CONSUMER GROUP group7 ADD USER ysj_user7;
ALTER CONSUMER GROUP group8 ADD USER ysj_user8;
ALTER CONSUMER GROUP group9 ADD USER ysj_user9;
ALTER CONSUMER GROUP group10 ADD USER ysj_user10;

-- 创建静态资源池 
-- max_disk_space:该资源池关联的所有用户的表空间占用磁盘总和，设置单位为MB 19T*1024/10=1945.6
CREATE RESOURCE POOL static_pool1(
    cpu_percent=9, -- 100%
	max_memory=222822, --  157286  +  65536
	max_temp_diskspace=734, --  36700160 * 2 
	max_disk_space=1945, --  36700160  * 2 
	max_disk_writeio=1000,
	max_disk_readio=1000
) TYPE STATIC;

CREATE RESOURCE POOL static_pool2(
    cpu_percent=9, -- 100%
	max_memory=222822, --  157286  +  65536
	max_temp_diskspace=734, --  36700160 * 2 
	max_disk_space=1945, --  36700160  * 2 
	max_disk_writeio=1000,
	max_disk_readio=1000
) TYPE STATIC;

CREATE RESOURCE POOL static_pool3(
    cpu_percent=9, -- 100%
	max_memory=222822, --  157286  +  65536
	max_temp_diskspace=734, --  36700160 * 2 
	max_disk_space=1945, --  36700160  * 2 
	max_disk_writeio=1000,
	max_disk_readio=1000
) TYPE STATIC;

CREATE RESOURCE POOL static_pool4(
    cpu_percent=9, -- 100%
	max_memory=222822, --  157286  +  65536
	max_temp_diskspace=734, --  36700160 * 2 
	max_disk_space=1945, --  36700160  * 2 
	max_disk_writeio=1000,
	max_disk_readio=1000
) TYPE STATIC;

CREATE RESOURCE POOL static_pool5(
    cpu_percent=9, -- 100%
	max_memory=222822, --  157286  +  65536
	max_temp_diskspace=734, --  36700160 * 2 
	max_disk_space=1945, --  36700160  * 2 
	max_disk_writeio=1000,
	max_disk_readio=1000
) TYPE STATIC;

CREATE RESOURCE POOL static_pool6(
    cpu_percent=9, -- 100%
	max_memory=222822, --  157286  +  65536
	max_temp_diskspace=734, --  36700160 * 2 
	max_disk_space=1945, --  36700160  * 2 
	max_disk_writeio=1000,
	max_disk_readio=1000
) TYPE STATIC;

CREATE RESOURCE POOL static_pool7(
    cpu_percent=9, -- 100%
	max_memory=222822, --  157286  +  65536
	max_temp_diskspace=734, --  36700160 * 2 
	max_disk_space=1945, --  36700160  * 2 
	max_disk_writeio=1000,
	max_disk_readio=1000
) TYPE STATIC;

CREATE RESOURCE POOL static_pool8(
    cpu_percent=9, -- 100%
	max_memory=222822, --  157286  +  65536
	max_temp_diskspace=734, --  36700160 * 2 
	max_disk_space=1945, --  36700160  * 2 
	max_disk_writeio=1000,
	max_disk_readio=1000
) TYPE STATIC;

CREATE RESOURCE POOL static_pool9(
    cpu_percent=9, -- 100%
	max_memory=222822, --  157286  +  65536
	max_temp_diskspace=734, --  36700160 * 2 
	max_disk_space=1945, --  36700160  * 2 
	max_disk_writeio=1000,
	max_disk_readio=1000
) TYPE STATIC;

CREATE RESOURCE POOL static_pool10(
    cpu_percent=9, -- 100%
	max_memory=222822, --  157286  +  65536
	max_temp_diskspace=734, --  36700160 * 2 
	max_disk_space=1945, --  36700160  * 2 
	max_disk_writeio=1000,
	max_disk_readio=1000
) TYPE STATIC;

-- 创建动态资源池
CREATE RESOURCE POOL dynamic_pool1(  
	cpu_percent=100,  --  使用40%的cpu
	max_memory=222822, --  使用64G内存
	max_temp_diskspace=734, --  35T 
	max_disk_space=1945, -- 35T 
	max_disk_writeio=1000,  -- 10G
	max_disk_readio=1000    -- 10G
) TYPE DYNAMIC BASE ON static_pool1; 

CREATE RESOURCE POOL dynamic_pool2(  
	cpu_percent=100,  --  使用40%的cpu
	max_memory=222822, --  使用64G内存
	max_temp_diskspace=734, --  35T 
	max_disk_space=1945, -- 35T 
	max_disk_writeio=1000,  -- 10G
	max_disk_readio=1000    -- 10G
) TYPE DYNAMIC BASE ON static_pool2; 

CREATE RESOURCE POOL dynamic_pool3(  
	cpu_percent=100,  --  使用40%的cpu
	max_memory=222822, --  使用64G内存
	max_temp_diskspace=734, --  35T 
	max_disk_space=1945, -- 35T 
	max_disk_writeio=1000,  -- 10G
	max_disk_readio=1000    -- 10G 
) TYPE DYNAMIC BASE ON static_pool3;

CREATE RESOURCE POOL dynamic_pool4(  
	cpu_percent=100,  --  使用40%的cpu
	max_memory=222822, --  使用64G内存
	max_temp_diskspace=734, --  35T 
	max_disk_space=1945, -- 35T 
	max_disk_writeio=1000,  -- 10G
	max_disk_readio=1000    -- 10G
) TYPE DYNAMIC BASE ON static_pool4; 

CREATE RESOURCE POOL dynamic_pool5(  
	cpu_percent=100,  --  使用40%的cpu
	max_memory=222822, --  使用64G内存
	max_temp_diskspace=734, --  35T 
	max_disk_space=1945, -- 35T 
	max_disk_writeio=1000,  -- 10G
	max_disk_readio=1000    -- 10G
) TYPE DYNAMIC BASE ON static_pool5; 

CREATE RESOURCE POOL dynamic_pool6(  
	cpu_percent=100,  --  使用40%的cpu
	max_memory=222822, --  使用64G内存
	max_temp_diskspace=734, --  35T 
	max_disk_space=1945, -- 35T 
	max_disk_writeio=1000,  -- 10G
	max_disk_readio=1000    -- 10G
) TYPE DYNAMIC BASE ON static_pool6; 

CREATE RESOURCE POOL dynamic_pool7(  
	cpu_percent=100,  --  使用40%的cpu
	max_memory=222822, --  使用64G内存
	max_temp_diskspace=734, --  35T 
	max_disk_space=1945, -- 35T 
	max_disk_writeio=1000,  -- 10G
	max_disk_readio=1000    -- 10G
) TYPE DYNAMIC BASE ON static_pool7; 

CREATE RESOURCE POOL dynamic_pool8(  
	cpu_percent=100,  --  使用40%的cpu
	max_memory=222822, --  使用64G内存
	max_temp_diskspace=734, --  35T 
	max_disk_space=1945, -- 35T 
	max_disk_writeio=1000,  -- 10G
	max_disk_readio=1000    -- 10G
) TYPE DYNAMIC BASE ON static_pool8; 

CREATE RESOURCE POOL dynamic_pool9(  
	cpu_percent=100,  --  使用40%的cpu
	max_memory=222822, --  使用64G内存
	max_temp_diskspace=734, --  35T 
	max_disk_space=1945, -- 35T 
	max_disk_writeio=1000,  -- 10G
	max_disk_readio=1000    -- 10G
) TYPE DYNAMIC BASE ON static_pool9; 

CREATE RESOURCE POOL dynamic_pool10(  
	cpu_percent=100,  --  使用40%的cpu
	max_memory=222822, --  使用64G内存
	max_temp_diskspace=734, --  35T 
	max_disk_space=1945, -- 35T 
	max_disk_writeio=1000,  -- 10G
	max_disk_readio=1000    -- 10G
) TYPE DYNAMIC BASE ON static_pool10; 

-- 创建资源计划
CREATE RESOURCE PLAN source_plan comment = 'source_plan';

-- 创建资源指令（将用户自定义资源消费组与动态资源池关联）
CREATE RESOURCE DIRECTIVE directive1 (
	plan_name = 'source_plan',
	group_name = 'group1',
	pool_name = 'dynamic_pool1',
	comment = 'directive1'
);

CREATE RESOURCE DIRECTIVE directive2 (
	plan_name = 'source_plan',
	group_name = 'group2',
	pool_name = 'dynamic_pool2',
	comment = 'directive2'
);

CREATE RESOURCE DIRECTIVE directive3 (
	plan_name = 'source_plan',
	group_name = 'group3',
	pool_name = 'dynamic_pool3',
	comment = 'directive3'
);

CREATE RESOURCE DIRECTIVE directive4 (
	plan_name = 'source_plan',
	group_name = 'group4',
	pool_name = 'dynamic_pool4',
	comment = 'directive4'
);

CREATE RESOURCE DIRECTIVE directive5 (
	plan_name = 'source_plan',
	group_name = 'group5',
	pool_name = 'dynamic_pool5',
	comment = 'directive5'
);

CREATE RESOURCE DIRECTIVE directive6 (
	plan_name = 'source_plan',
	group_name = 'group6',
	pool_name = 'dynamic_pool6',
	comment = 'directive6'
);

CREATE RESOURCE DIRECTIVE directive7 (
	plan_name = 'source_plan',
	group_name = 'group7',
	pool_name = 'dynamic_pool7',
	comment = 'directive7'
);

CREATE RESOURCE DIRECTIVE directive8 (
	plan_name = 'source_plan',
	group_name = 'group8',
	pool_name = 'dynamic_pool8',
	comment = 'directive8'
);

CREATE RESOURCE DIRECTIVE directive9 (
	plan_name = 'source_plan',
	group_name = 'group9',
	pool_name = 'dynamic_pool9',
	comment = 'directive9'
);

CREATE RESOURCE DIRECTIVE directive10 (
	plan_name = 'source_plan',
	group_name = 'group10',
	pool_name = 'dynamic_pool10',
	comment = 'directive10'
);

-- 创建默认的资源池（100%磁盘 100CPU）
CREATE RESOURCE POOL static_default(
    cpu_percent=9, -- 100%
	max_memory=222822, --  157286  +  65536
	max_temp_diskspace=734, --  36700160 * 2 
	max_disk_space=1945, --  36700160  * 2 
	max_disk_writeio=1000,
	max_disk_readio=1000
) TYPE STATIC;

CREATE RESOURCE POOL dynamic_default(  
	cpu_percent=100,  --  使用40%的cpu
	max_memory=222822, --  使用64G内存
	max_temp_diskspace=734, --  35T 
	max_disk_space=1945, -- 35T 
	max_disk_writeio=1000,  -- 10G
	max_disk_readio=1000    -- 10G
) TYPE DYNAMIC BASE ON static_default; 

create resource DIRECTIVE directive_default (
	plan_name = 'source_plan',
	group_name = 'default_consumer_group',
	pool_name = 'dynamic_default',
	comment = 'dynamic_default directive'
);

--激活
ACTIVE RESOURCE PLAN source_plan ON VC vcname000001;


/*
	AKshare 数据
*/
--01个股信息查询
DROP TABLE stock_individual_info;
CREATE TABLE IF NOT EXISTS stock_individual_info (
  trade_data DATE DEFAULT NULL COMMENT '交易日期',
  symbol_code BIGINT DEFAULT NULL COMMENT '股票代码',
  symbol_name VARCHAR(64) DEFAULT NULL COMMENT '股票简称',
  total_share BIGINT DEFAULT NULL COMMENT '总股本',
  float_share BIGINT DEFAULT NULL COMMENT '流通股本',
  total_mv DECIMAL(16,2) DEFAULT NULL COMMENT '总市值',
  circ_mv DECIMAL(16,2) DEFAULT NULL COMMENT '流通市值',
  industry VARCHAR(64) DEFAULT NULL COMMENT '行业类别',
  list_date DATE DEFAULT NULL COMMENT '上市时间'
) DISTRIBUTED BY('symbol_code') COMMENT '个股信息查询';

LOAD DATA INFILE 'file://192.168.105.35/tmp/stock_individual_info.txt' INTO TABLE stock_individual_info DATA_FORMAT 3 FIELDS TERMINATED BY '|';


--02实时行情数据-东财
DROP TABLE stock_zh_a_spot;
CREATE TABLE IF NOT EXISTS stock_zh_a_spot (
  trade_date DATE DEFAULT NULL COMMENT '交易日期',
  symbol_code BIGINT DEFAULT NULL COMMENT '代码',
  symbol_name VARCHAR(50) DEFAULT NULL COMMENT '名称',
  curent_price DECIMAL(16,2) DEFAULT NULL COMMENT '最新价',
  pct_change DECIMAL(16,2) DEFAULT NULL COMMENT '涨跌幅',
  change1 DECIMAL(16,2) DEFAULT NULL COMMENT '涨跌额',
  high DECIMAL(16,2) DEFAULT NULL COMMENT '最高',
  low DECIMAL(16,2) DEFAULT NULL COMMENT '最低',
  OpenPrice DECIMAL(16,2) DEFAULT NULL COMMENT '今开',
  PreClosePrice DECIMAL(16,2) DEFAULT NULL COMMENT '昨收',
  pct_volumn DECIMAL(16,2) DEFAULT NULL COMMENT '量比',
  turnover DECIMAL(16,2) DEFAULT NULL COMMENT '换手率',
  pe DECIMAL(16,2) DEFAULT NULL COMMENT '市盈率',
  pb DECIMAL(16,2) DEFAULT NULL COMMENT '市净率',
  total_mv DECIMAL(16,2) DEFAULT NULL COMMENT '总市值',
  circ_mv DECIMAL(16,2) DEFAULT NULL COMMENT '流通市值'
) DISTRIBUTED BY('symbol_code') COMMENT '实时行情数据';

LOAD DATA INFILE 'file://192.168.105.35/tmp/stock_zh_a_spot.txt' INTO TABLE stock_zh_a_spot DATA_FORMAT 3 FIELDS TERMINATED BY '|';


--03历史行情数据-东财
DROP TABLE stock_zh_a_hist;
CREATE TABLE IF NOT EXISTS stock_zh_a_hist (
  symbol_code BIGINT DEFAULT NULL COMMENT '股票代码',
  trade_date DATE DEFAULT NULL COMMENT '日期',
  open DECIMAL(16,2) DEFAULT NULL COMMENT '开盘',
  close DECIMAL(16,2) DEFAULT NULL COMMENT '收盘',
  high DECIMAL(16,2) DEFAULT NULL COMMENT '最高',
  low DECIMAL(16,2) DEFAULT NULL COMMENT '最低',
  volumn BIGINT DEFAULT NULL COMMENT '交易量',
  amount DECIMAL(16,2) DEFAULT NULL COMMENT '交易额',
  swing DECIMAL(16,2) DEFAULT NULL COMMENT '振幅',
  pct_change DECIMAL(16,2) DEFAULT NULL COMMENT '涨跌幅',
  pct_amount DECIMAL(16,2) DEFAULT NULL COMMENT '涨跌额',
  turn_over DECIMAL(16,2) DEFAULT NULL COMMENT '换手率'
) DISTRIBUTED BY('symbol_code') COMMENT '历史行情数据';

LOAD DATA INFILE 'file://192.168.105.35/tmp/stock_zh_a_hist.txt' INTO TABLE stock_zh_a_hist DATA_FORMAT 3 FIELDS TERMINATED BY '|';


DROP TABLE stock_zh_a_hist_partition;
CREATE TABLE IF NOT EXISTS stock_zh_a_hist_partition (
  symbol_code BIGINT DEFAULT NULL COMMENT '股票代码',
  trade_date DATE DEFAULT NULL COMMENT '日期',
  open DECIMAL(16,2) DEFAULT NULL COMMENT '开盘',
  close DECIMAL(16,2) DEFAULT NULL COMMENT '收盘',
  high DECIMAL(16,2) DEFAULT NULL COMMENT '最高',
  low DECIMAL(16,2) DEFAULT NULL COMMENT '最低',
  volumn BIGINT DEFAULT NULL COMMENT '交易量',
  amount DECIMAL(16,2) DEFAULT NULL COMMENT '交易额',
  swing DECIMAL(16,2) DEFAULT NULL COMMENT '振幅',
  pct_change DECIMAL(16,2) DEFAULT NULL COMMENT '涨跌幅',
  pct_amount DECIMAL(16,2) DEFAULT NULL COMMENT '涨跌额',
  turn_over DECIMAL(16,2) DEFAULT NULL COMMENT '换手率'
)
DISTRIBUTED BY('symbol_code') COMMENT '历史行情数据分区表'
PARTITION BY RANGE(year(trade_date))
(
    PARTITION p0 values less than (2022),
    PARTITION p1 values less than (2023),
    PARTITION p2 values less than (2024),
    PARTITION p3 values less than (2025)
);


--04个股新闻
DROP TABLE stock_news;
CREATE TABLE IF NOT EXISTS stock_news (
  symbol_code BIGINT DEFAULT NULL COMMENT '关键词',
  news_title VARCHAR(50) DEFAULT NULL COMMENT '新闻标题',
  news_sentence VARCHAR(500) DEFAULT NULL COMMENT '新闻内容',
  announce_date DATE DEFAULT NULL COMMENT '发布时间',
  news_source VARCHAR(50) DEFAULT NULL COMMENT '文章来源'
) DISTRIBUTED BY('symbol_code') COMMENT '个股新闻';

LOAD DATA INFILE 'file://192.168.105.35/tmp/stock_news.txt' INTO TABLE stock_news DATA_FORMAT 3 FIELDS TERMINATED BY '|';


--05业绩报表
DROP TABLE stock_yjbb;
CREATE TABLE IF NOT EXISTS stock_yjbb (
  symbol_code BIGINT DEFAULT NULL COMMENT '股票代码',
  symbol_name VARCHAR(64) DEFAULT NULL COMMENT '股票简称',
  diluted_eps DECIMAL(16,2) DEFAULT NULL COMMENT '每股收益',
  revenue DECIMAL(16,2) DEFAULT NULL COMMENT '营业收入',
  n_income DECIMAL(16,2) DEFAULT NULL COMMENT '净利润',
  industry VARCHAR(64) DEFAULT NULL COMMENT '所处行业',
  announce_date DATE DEFAULT NULL COMMENT '最新公告日期'
) DISTRIBUTED BY('symbol_code') COMMENT '业绩报表';

LOAD DATA INFILE 'file://192.168.105.35/tmp/stock_yjbb.txt' INTO TABLE stock_yjbb DATA_FORMAT 3 FIELDS TERMINATED BY '|';


--06盈利预测
DROP TABLE stock_profit_forecast;
CREATE TABLE IF NOT EXISTS stock_profit_forecast (
  symbol_code BIGINT DEFAULT NULL COMMENT '代码',
  symbol_name VARCHAR(50) DEFAULT NULL COMMENT '名称',
  report_number INT DEFAULT NULL COMMENT '研报数',
  eps_2023 DECIMAL(16,2) DEFAULT NULL COMMENT '2023预测每股收益',
  eps_2024 DECIMAL(16,2) DEFAULT NULL COMMENT '2024预测每股收益',
  eps_2025 DECIMAL(16,2) DEFAULT NULL COMMENT '2025预测每股收益',
  eps_2026 DECIMAL(16,2) DEFAULT NULL COMMENT '2026预测每股收益'
) DISTRIBUTED BY('symbol_code') COMMENT '板块信息';

LOAD DATA INFILE 'file://192.168.105.35/tmp/stock_profit_forecast.txt' INTO TABLE stock_profit_forecast DATA_FORMAT 3 FIELDS TERMINATED BY '|';


--07行业一览表
DROP TABLE stock_board_industry_summary_ths;
CREATE TABLE IF NOT EXISTS stock_board_industry_summary_ths (
  industry VARCHAR(50) DEFAULT NULL COMMENT '板块',
  pct_change DECIMAL(16,2) DEFAULT NULL COMMENT '涨跌幅',
  open DECIMAL(16,2) DEFAULT NULL COMMENT '总成交量',
  close DECIMAL(16,2) DEFAULT NULL COMMENT '总成交额',
  high DECIMAL(16,2) DEFAULT NULL COMMENT '净流入',
  low DECIMAL(16,2) DEFAULT NULL COMMENT '均价'
) DISTRIBUTED BY('industry') COMMENT '板块信息';

LOAD DATA INFILE 'file://192.168.105.35/tmp/stock_board_industry_summary_ths.txt' INTO TABLE stock_board_industry_summary_ths DATA_FORMAT 3 FIELDS TERMINATED BY '|';

/*
	存储过程和函数
*/

DROP FUNCTION count_add;

DELIMITER //
CREATE FUNCTION count_add (V_ID INTEGER) RETURNS INTEGER
BEGIN
	RETURN V_ID *2;
END //

SELECT symbol_code,count_add(symbol_code) FROM stock_news;