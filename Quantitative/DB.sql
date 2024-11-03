gccli -ugbase -pX@gbase2018 -Dvcname000001.mydb -f < /tmp/1.sql

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

LOAD DATA INFILE 'file://192.168.31.35/tmp/stock_individual_info.txt' INTO TABLE stock_individual_info DATA_FORMAT 3 FIELDS TERMINATED BY '|';


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

LOAD DATA INFILE 'file://192.168.31.35/tmp/stock_zh_a_spot.txt' INTO TABLE stock_zh_a_spot DATA_FORMAT 3 FIELDS TERMINATED BY '|';


--03历史行情数据-东财
'股票代码','日期', '开盘', '收盘', '最高', '最低','成交量','成交额','振幅','涨跌幅','涨跌额','换手率'

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

LOAD DATA INFILE 'file://192.168.31.35/tmp/stock_zh_a_hist.txt' INTO TABLE stock_zh_a_hist DATA_FORMAT 3 FIELDS TERMINATED BY '|';


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
)
;


--04个股新闻
DROP TABLE stock_news;
CREATE TABLE IF NOT EXISTS stock_news (
  symbol_code BIGINT DEFAULT NULL COMMENT '关键词',
  news_title VARCHAR(50) DEFAULT NULL COMMENT '新闻标题',
  news_sentence VARCHAR(500) DEFAULT NULL COMMENT '新闻内容',
  announce_date DATE DEFAULT NULL COMMENT '发布时间',
  news_source VARCHAR(50) DEFAULT NULL COMMENT '文章来源'
) DISTRIBUTED BY('symbol_code') COMMENT '个股新闻';

LOAD DATA INFILE 'file://192.168.31.35/tmp/stock_news.txt' INTO TABLE stock_news DATA_FORMAT 3 FIELDS TERMINATED BY '|';


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

LOAD DATA INFILE 'file://192.168.31.35/tmp/stock_yjbb.txt' INTO TABLE stock_yjbb DATA_FORMAT 3 FIELDS TERMINATED BY '|';


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

LOAD DATA INFILE 'file://192.168.31.35/tmp/stock_profit_forecast.txt' INTO TABLE stock_profit_forecast DATA_FORMAT 3 FIELDS TERMINATED BY '|';


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

LOAD DATA INFILE 'file://192.168.31.35/tmp/stock_board_industry_summary_ths.txt' INTO TABLE stock_board_industry_summary_ths DATA_FORMAT 3 FIELDS TERMINATED BY '|';

####################################################################

gccli -ugbase -p123456 -Dvcname000001.mydb

truncate table stock_news2;
insert into stock_news2 select * from stock_news;
insert into stock_news2 select * from stock_news2;
insert into stock_news2 select * from stock_news2;

SELECT news_source,ROW_NUMBER() OVER (PARTITION BY news_source ORDER BY news_source DESC) FROM stock_news2 limit 20;

insert into stock_zh_a_hist_partition select * from stock_zh_a_hist;
insert into stock_zh_a_hist_partition select * from stock_zh_a_hist_partition;

select year(trade_date),count(1) from stock_zh_a_hist_partition group by 1;
select symbol_code,year(trade_date),count(1) from stock_zh_a_hist_partition group by 1,2;

du -sh /opt/192.168.*/gnode/userdata/gbase/mydb/sys_tablespace/stock_zh_a_hist_partition*
du -s /opt/192.168.*/gnode/userdata/gbase/mydb/sys_tablespace/stock_zh_a_hist_partition* | awk '{print $1}'

select * from TABLES where table_schema ='mydb' and table_name='stock_zh_a_hist_partition';

-- 非分区表单位KB 比较准
gbase> select STORAGE_SIZE/1024 from TABLES where table_schema ='mydb' and table_name='stock_zh_a_hist'\G
