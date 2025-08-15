SELECT * FROM crime_scene_reports 
WHERE year = 2023 AND month = 7 AND day = 28 
AND street = 'Humphrey Street';


SELECT * FROM interviews 
WHERE year = 2023 AND month = 7 AND day = 28
AND transcript LIKE '%bakery%';
295|2023|7|28|Humphrey Street|CS50鸭子的盗窃案发生在上午10:15在汉弗莱街面包店。今天对当时在场的三名目击者进行了采访 - 他们的每份采访记录都提到了面包店。
297|2023|7|28|Humphrey Street|乱扔垃圾发生在16:36。没有已知目击者。


sqlite> SELECT * FROM interviews WHERE year = 2023 AND month = 7 AND day = 28 AND transcript LIKE '%bakery%';
161|Ruth|2023|7|28|在盗窃案发生后的十分钟内，我看到小偷在面包店停车场上了一辆车然后开走了。如果你有面包店停车场的监控录像，你可能想要查看在那个时间段离开停车场的车辆。
162|Eugene|2023|7|28|我不知道小偷的名字，但那是我认识的人。今天早上早些时候，在我到达Emma's面包店之前，我路过Leggett Street的ATM时看到小偷在那里取钱。
163|Raymond|2023|7|28|当小偷离开面包店时，他们给某人打了电话，通话时间不到一分钟。在通话中，我听到小偷说他们计划明天乘坐最早的航班离开Fiftyville。然后小偷要求电话另一端的人购买机票。

-- ATM取钱记录查询 (案发前10:15在Leggett Street)
SELECT * FROM atm_transactions 
WHERE year = 2023 AND month = 7 AND day = 28 
AND atm_location = 'Leggett Street' 
AND transaction_type = 'withdraw';

246|28500762|2023|7|28|Leggett Street|withdraw|48
264|28296815|2023|7|28|Leggett Street|withdraw|20
266|76054385|2023|7|28|Leggett Street|withdraw|60
267|49610011|2023|7|28|Leggett Street|withdraw|50
269|16153065|2023|7|28|Leggett Street|withdraw|80
288|25506511|2023|7|28|Leggett Street|withdraw|20
313|81061156|2023|7|28|Leggett Street|withdraw|30
336|26013199|2023|7|28|Leggett Street|withdraw|35


SELECT atm.*, people.id as person_id, people.name
FROM atm_transactions atm
JOIN bank_accounts ba ON atm.account_number = ba.account_number  
JOIN people ON ba.person_id = people.id
WHERE atm.year = 2023 AND atm.month = 7 AND atm.day = 28 
AND atm.atm_location = 'Leggett Street' 
AND atm.transaction_type = 'withdraw';

267|49610011|2023|7|28|Leggett Street|withdraw|50|686048|Bruce
336|26013199|2023|7|28|Leggett Street|withdraw|35|514354|Diana
269|16153065|2023|7|28|Leggett Street|withdraw|80|458378|Brooke
264|28296815|2023|7|28|Leggett Street|withdraw|20|395717|Kenny
288|25506511|2023|7|28|Leggett Street|withdraw|20|396669|Iman
246|28500762|2023|7|28|Leggett Street|withdraw|48|467400|Luca
266|76054385|2023|7|28|Leggett Street|withdraw|60|449774|Taylor
313|81061156|2023|7|28|Leggett Street|withdraw|30|438727|Benista

小偷说他们计划明天乘坐最早的航班离开Fiftyville，所以查询最早的航班
SELECT * FROM flights
WHERE year = 2023 AND month = 7 AND day = 29
ORDER BY hour, minute
LIMIT 1;
36|8|4|2023|7|29|8|20
解释表数据：
id: 航班编号
origin_airport_id: 出发机场编号
destination_airport_id: 到达机场编号
year: 年
month: 月
day: 日
hour: 小时
minute: 分钟



163|Raymond|2023|7|28|当小偷离开面包店时，他们给某人打了电话，通话时间不到一分钟。在通话中，我听到小偷说他们计划明天乘坐最早的航班离开Fiftyville。然后小偷要求电话另一端的人购买机票。
- 小偷打电话给同伙，同伙购买了机票

-- 查询7月28日通话时间小于1分钟的电话记录
SELECT 
    pc.*,
    p1.name as caller_name,
    p2.name as receiver_name
FROM phone_calls pc
LEFT JOIN people p1 ON pc.caller = p1.phone_number
LEFT JOIN people p2 ON pc.receiver = p2.phone_number
WHERE pc.year = 2023 AND pc.month = 7 AND pc.day = 28
AND pc.duration < 60;

221|(130) 555-0289|(996) 555-8899|2023|7|28|51|Sofia|Jack
224|(499) 555-9472|(892) 555-8872|2023|7|28|36|Kelsey|Larry
233|(367) 555-5533|(375) 555-8161|2023|7|28|45|Bruce|Robin
251|(499) 555-9472|(717) 555-1342|2023|7|28|50|Kelsey|Melissa
254|(286) 555-6063|(676) 555-6554|2023|7|28|43|Taylor|James
255|(770) 555-1861|(725) 555-3243|2023|7|28|49|Diana|Philip
261|(031) 555-6622|(910) 555-3251|2023|7|28|38|Carina|Jacqueline
279|(826) 555-1652|(066) 555-9701|2023|7|28|55|Kenny|Doris
281|(338) 555-6650|(704) 555-2131|2023|7|28|54|Benista|Anna








-- 查询7月29日最早航班(id=36)的乘客信息
-- 这些乘客中包含小偷，因为小偷计划乘坐最早的航班逃离

SELECT 
    f.id as flight_id,
    p.passport_number,
    p.name,
    pa.seat
FROM flights f
JOIN passengers pa ON f.id = pa.flight_id
JOIN people p ON pa.passport_number = p.passport_number
WHERE f.id = 36;

36|7214083635|Doris|2A
36|1695452385|Sofia|3B
36|5773159633|Bruce|4A
36|1540955065|Edward|5C
36|8294398571|Kelsey|6C
36|1988161715|Taylor|6D
36|9878712108|Kenny|7A
36|8496433585|Luca|7B

-- 查找交集：既在航班36上又在7月28日打电话的人
-- 航班36乘客: Doris, Sofia, Bruce, Edward, Kelsey, Taylor, Kenny, Luca
-- 电话记录中的人: Sofia, Kelsey, Bruce, Taylor, Kenny

-- 交集分析:
-- Sofia: 航班乘客 + 电话记录中的caller
-- Kelsey: 航班乘客 + 电话记录中的caller (打了2通电话)
-- Bruce: 航班乘客 + 电话记录中的caller + ATM取款记录
-- Taylor: 航班乘客 + 电话记录中的caller + ATM取款记录
-- Kenny: 航班乘客 + 电话记录中的caller + ATM取款记录

-- 可疑人员: Sofia, Kelsey, Bruce, Taylor, Kenny
-- 最可疑人员(同时有ATM记录): Bruce, Taylor, Kenny


CREATE TABLE bakery_security_logs (
    id INTEGER,
    year INTEGER,
    month INTEGER,
    day INTEGER,
    hour INTEGER,
    minute INTEGER,
    activity TEXT,
    license_plate TEXT,
    PRIMARY KEY(id)
);

查找案发时间(10:15)前后的车辆活动：
SELECT DISTINCT people.name, people.license_plate, bsl.*
FROM bakery_security_logs bsl
JOIN people ON bsl.license_plate = people.license_plate
WHERE bsl.year = 2023 AND bsl.month = 7 AND bsl.day = 28;

查找案发时间(10:15)前后的车辆活动：
SELECT people.name, people.license_plate, bsl.activity, bsl.hour, bsl.minute
FROM bakery_security_logs bsl
JOIN people ON bsl.license_plate = people.license_plate
WHERE bsl.year = 2023 AND bsl.month = 7 AND bsl.day = 28
AND (bsl.hour > 10 OR (bsl.hour = 10 AND bsl.minute >= 15));



-- 案发时间(10:15)后离开面包店的车辆记录：
Vanessa|5P2BI95|exit|10|16
Bruce|94KL13X|exit|10|18     -- ★ 最可疑！航班乘客+电话记录+ATM取款+案发后立即离开
Barry|6P58WS2|exit|10|18
Luca|4328GD8|exit|10|19
Sofia|G412CB7|exit|10|20
Iman|L93JTIZ|exit|10|21
Diana|322W7JE|exit|10|23
Kelsey|0NTHK55|exit|10|23
Taylor|1106N58|exit|10|35    -- ★ 可疑！航班乘客+电话记录+ATM取款+案发后离开
Denise|NRYN856|entrance|10|42
Thomas|WD5M8I6|entrance|10|44
Jeremy|V47T75I|entrance|10|55
Judith|4963D92|entrance|11|6
Mary|C194752|entrance|11|13
Vincent|94MV71O|entrance|11|52
Daniel|FLFN3W0|entrance|12|20
Frank|207W38T|entrance|12|49
Amanda|RS7I6A0|entrance|13|8
John|4468KVT|entrance|13|30
Ethan|NAW9653|entrance|13|42
Ethan|NAW9653|exit|14|18
Amanda|RS7I6A0|exit|15|6
Vincent|94MV71O|exit|15|16
Thomas|WD5M8I6|exit|16|6
John|4468KVT|exit|16|38
Frank|207W38T|exit|16|42
Mary|C194752|exit|16|47
Denise|NRYN856|exit|17|11
Sophia|13FNH73|exit|17|15
Jeremy|V47T75I|exit|17|16
Brandon|R3G7486|exit|17|18
Daniel|FLFN3W0|exit|17|36
Judith|4963D92|exit|17|47

-- 分析：
-- Bruce: 10:18离开(案发后3分钟) - 航班36乘客+电话caller+ATM取款 = 最高嫌疑
-- Taylor: 10:35离开(案发后20分钟) - 航班36乘客+电话caller+ATM取款 = 高嫌疑  
-- Kenny: 未出现在面包店记录中，排除嫌疑

-- 查询Bruce的电话记录
SELECT * FROM phone_calls
WHERE caller = '(367) 555-5533';

9|(367) 555-5533|(113) 555-7544|2023|7|25|469
104|(367) 555-5533|(238) 555-5554|2023|7|26|84
122|(367) 555-5533|(660) 555-3095|2023|7|26|399
133|(367) 555-5533|(286) 555-0131|2023|7|26|444
233|(367) 555-5533|(375) 555-8161|2023|7|28|45
236|(367) 555-5533|(344) 555-9601|2023|7|28|120
245|(367) 555-5533|(022) 555-4052|2023|7|28|241
285|(367) 555-5533|(704) 555-5790|2023|7|28|75
395|(367) 555-5533|(455) 555-5315|2023|7|30|31
418|(367) 555-5533|(841) 555-3728|2023|7|30|511
488|(367) 555-5533|(696) 555-9195|2023|7|31|261




