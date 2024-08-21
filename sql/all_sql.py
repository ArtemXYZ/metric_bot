"""
Здесь содержатся все запросы sql
"""


save_stat = """
INSERT INTO division.metric_bot_stat (dt, user_id, metric, answer_type) VALUES ('{0}', '{1}', '{2}', '{3}')
"""



#  Тип данных столбца tg в базе данных — это строка, не пердавать в запросе значение в виде целого числа !
tg_id_jar = """SELECT code as user_id FROM inlet.staff_for_bot WHERE tg = '{0}'"""


user_data_gp_mart_sv = """
SELECT
    emp_type as role, emp_guid as guid 
FROM 
    mart_sv.employees_position_for_bot 
WHERE
    emp_code_1c = '{0}'
"""

# Вернет 1 значение
kpd_user = """
SELECT 
        kpd 
FROM 
    (SELECT 
            InvoiceTime + PaymentTime + ReturnTime + GivedTime + ArrivalTime + ShipmentTime + 
            BillingTime + WorkCarTime + ReevaluationTime + DustingTime + CleaningTime + ServisTime +            
            InventoryTime + GroupGoodsTime + (((InvoiceCnt * 2)*240)/3600) + OnlineOrdersTime + ActualTime +           
            ExchangeTime + ZReportTime as fact,
            ReportCard as tabel,
            fact/ tabel as kpd
    FROM 
            ch_sv."KPD_Motivation_monitoring_of_staff_workload" as kpd
    WHERE 
            UserGuid = '{0}'
        and 
            CurrentPeriod = toStartOfMonth(now())
    ) as kpd
"""

# Вернет массив
# kpd_rating = """
# with kpd as
#         (
#             SELECT
#                     UserName,
#                     UserGuid,
#                     InvoiceTime + PaymentTime + ReturnTime + GivedTime + ArrivalTime + ShipmentTime +
#                     BillingTime + WorkCarTime + ReevaluationTime + DustingTime + CleaningTime + ServisTime +
#                     InventoryTime + GroupGoodsTime + (((InvoiceCnt * 2)*240)/3600) + OnlineOrdersTime + ActualTime +
#                     ExchangeTime + ZReportTime as fact,
#                     ReportCard as tabel,
#                     fact / tabel as kpd
#                     ,rank() over (order by kpd desc) as rating_kpd
#             FROM
#                     ch_sv.KPD_Motivation_monitoring_of_staff_workload kpd
#             WHERE
#                     RDCName = (
#                                 SELECT
#                                 DISTINCT
#                                         RDCName as rrs
#                                 FROM
#                                         ch_sv.KPD_Motivation_monitoring_of_staff_workload
#                                 WHERE
#                                         UserGuid = '{0}'
#                                 )
#             and
#                     CurrentPeriod = toStartOfMonth(now())
#         )
#         SELECT
#                 UserName, kpd, rating_kpd from kpd limit 5
#         union all
#         SELECT
#                 UserName, kpd, rating_kpd from kpd where  UserGuid = '{0}'
#         UNION all
#         SELECT UserName, kpd, rating_kpd from kpd order by rating_kpd desc limit 5
# """



# 1. Вернет 3 значения: UserName, kpd, rating_kpd (kpd в текущем месяце).
kpd_rating_user = """
with kpd as 
        (
            SELECT 
                    UserName,
                    UserGuid,
                    InvoiceTime + PaymentTime + ReturnTime + GivedTime + ArrivalTime + ShipmentTime + 
                    BillingTime + WorkCarTime + ReevaluationTime + DustingTime + CleaningTime + ServisTime + 
                    InventoryTime + GroupGoodsTime + (((InvoiceCnt * 2)*240)/3600) + OnlineOrdersTime + ActualTime +
                    ExchangeTime + ZReportTime as fact,
                    ReportCard as tabel,
                    fact / tabel as kpd
                    ,rank() over (order by kpd desc) as rating_kpd
            FROM     
                    ch_sv.KPD_Motivation_monitoring_of_staff_workload kpd
            WHERE
                    RDCName = (
                                SELECT 
                                DISTINCT 
                                        RDCName as rrs 
                                FROM 
                                        ch_sv.KPD_Motivation_monitoring_of_staff_workload
                                WHERE
                                        UserGuid = '{0}'
                                )   
            and 
                    CurrentPeriod = toStartOfMonth(now())
        )
        SELECT 
                UserName, kpd, rating_kpd 
        FROM 
                kpd 
        WHERE
                UserGuid = '{0}'
"""

# 2. Вернет массив: UserName, kpd, rating_kpd (Топ 5 пользователей по рейтингу в текущем месяце).
top5_kpd_rating_users = """
with kpd as
        (
            SELECT
                    UserName,
                    UserGuid,
                    InvoiceTime + PaymentTime + ReturnTime + GivedTime + ArrivalTime + ShipmentTime +
                    BillingTime + WorkCarTime + ReevaluationTime + DustingTime + CleaningTime + ServisTime +
                    InventoryTime + GroupGoodsTime + (((InvoiceCnt * 2)*240)/3600) + OnlineOrdersTime + ActualTime +
                    ExchangeTime + ZReportTime as fact,
                    ReportCard as tabel,
                    fact / tabel as kpd
                    ,rank() over (order by kpd desc) as rating_kpd
            FROM
                    ch_sv.KPD_Motivation_monitoring_of_staff_workload kpd
            WHERE
                    RDCName = (
                                SELECT
                                DISTINCT
                                        RDCName as rrs
                                FROM
                                        ch_sv.KPD_Motivation_monitoring_of_staff_workload
                                WHERE
                                        UserGuid = '{0}'
                                )
            and
                    CurrentPeriod = toStartOfMonth(now())
        )
        SELECT
                UserName, kpd, rating_kpd from kpd limit 5
        union all
        SELECT
                UserName, kpd, rating_kpd from kpd where  UserGuid = '{0}'
        UNION all
        SELECT UserName, kpd, rating_kpd from kpd order by rating_kpd desc limit 5
"""


# 3. Вернет массив: UserName, kpd, rating_kpd (Топ 5 с конца пользователей по рейтингу в текущем месяце).
top5end_kpd_rating_users = """
with kpd as
        (
            SELECT
                    UserName,
                    UserGuid,
                    InvoiceTime + PaymentTime + ReturnTime + GivedTime + ArrivalTime + ShipmentTime +
                    BillingTime + WorkCarTime + ReevaluationTime + DustingTime + CleaningTime + ServisTime +
                    InventoryTime + GroupGoodsTime + (((InvoiceCnt * 2)*240)/3600) + OnlineOrdersTime + ActualTime +
                    ExchangeTime + ZReportTime as fact,
                    ReportCard as tabel,
                    fact / tabel as kpd
                    ,rank() over (order by kpd desc) as rating_kpd
            FROM
                    ch_sv.KPD_Motivation_monitoring_of_staff_workload kpd
            WHERE
                    RDCName = (
                                SELECT
                                DISTINCT
                                        RDCName as rrs
                                FROM
                                        ch_sv.KPD_Motivation_monitoring_of_staff_workload
                                WHERE
                                        UserGuid = '{0}'
                                )
            and
                    CurrentPeriod = toStartOfMonth(now())
        )        
        SELECT UserName, kpd, rating_kpd 
        FROM
            kpd 
        order by 
            rating_kpd desc limit 5
"""





# Вернет 2 значения
# kpd_dinamic = """
# select
# 	kpd
# ,
# 	dt
# from
# 	(
# 	select
# 		CurrentPeriod as dt,
# 		InvoiceTime + PaymentTime +
# ReturnTime + GivedTime +
# ArrivalTime + ShipmentTime +
# BillingTime + WorkCarTime +
# ReevaluationTime + DustingTime +
# CleaningTime + ServisTime +
# InventoryTime + GroupGoodsTime +
# (((InvoiceCnt * 2)* 240)/ 3600)
# + OnlineOrdersTime + ActualTime +
# ExchangeTime + ZReportTime as fact,
# 		ReportCard as tabel,
# 		fact / tabel as kpd
# 	from
# 		ch_sv.KPD_Motivation_monitoring_of_staff_workload kpd
# 	where
# 		UserGuid = '{0}'
# 		and CurrentPeriod >= date_add(month,
# 		-6,
# 		toStartOfMonth(now()))
# 	) f
# """



# bot_table.tg in ({0})