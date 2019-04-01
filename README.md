# Peak Load Forecasting

## 1. Overview
根據台電歷史資料，預測未來七天的"電力尖峰負載"(MW)。

![](https://i.imgur.com/oiFgMtq.png)
[圖片來源](https://www.taipower.com.tw/d006/loadGraph/loadGraph/load_reserve_.html)


## 2. Goal
預測 2019/4/2 ~ 2019/4/8 的每日"電力尖峰負載"(MW)


## 3. 使用資料
 - [台灣電力公司_過去電力供需資訊](https://data.gov.tw/dataset/19995)
 - [今日預估尖峰備轉容量率](https://www.taipower.com.tw/d006/loadGraph/loadGraph/load_reserve_.html)
 - [觀測資料查詢系統](http://e-service.cwb.gov.tw/HistoryDataQuery/)
 - [中華民國一百零六年政府行政機關辦公日曆表](https://www.dgpa.gov.tw/information?uid=2&pid=4293)
 - [中華民國一百零七年政府行政機關辦公日曆表](https://www.dgpa.gov.tw/information?uid=83&pid=7473)
 - [中華民國108年（西元2019年）政府行政機關辦公日曆表](https://www.dgpa.gov.tw/information?uid=83&pid=8150)
 
 
## 4. 預測方法
尖峰負載與當天的溫度以及是否為平日成正相關，尤其連假期間越長，尖峰負載下降幅度越大。
因此分成兩個部分進行 LinearRegression，
上班日(補班日)和假日(週末與連假)，上班日使用溫度與星期，假日使用溫度與假期長度，



## 5. 檔案說明
 - data: 所有 CSV 資料
 - data: 所有資料整合後的 CSV
 - prepare_data.py: 將台電歷史資料、行事曆資料等等進行整合後儲存
 - app.py: 進行 LinearRegression，計算 Regression 後的 RMSE ，並對 2019/4/2 ~ 2019/4/8 預測，將結果儲存到 submission.csv
 
 
## 其他
有嘗試用Deep Learning來做但效果不如預期
[peak-load-forecasting-dl](https://github.com/nitsaick/peak-load-forecasting-dl)