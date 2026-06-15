# PitSight — DAX Measures Reference

All measures used in the Power BI dashboard. These reference Table 2 directly and work with disconnected lookup tables to avoid breaking the data model.

---

## Core Measures

### Satisfaction %
```dax
Satisfaction % = 
VAR _total = COUNTROWS(Table2)
VAR _satisfied = COUNTROWS(FILTER(Table2, Table2[Sentiment_Label] = "Satisfied"))
RETURN
IF(_total = 0, 0, DIVIDE(_satisfied, _total) * 100)
```

---

## Aspect Score Distribution (Disconnected Aspects Table)

### Aspects Table (Enter Data — no relationship)
| Aspect | Sort |
|--------|------|
| Maintenance | 1 |
| Comfort | 2 |
| Technology | 3 |
| Service | 4 |
| Fuel/Range | 5 |
| Performance | 6 |

### Negative %
```dax
Negative % = 
VAR asp = SELECTEDVALUE(Aspects[Aspect])
VAR total_maint = COUNTROWS(FILTER(Table2, Table2[maintenance_score] >= 1))
VAR total_comf = COUNTROWS(FILTER(Table2, Table2[comfort_score] >= 1))
VAR total_tech = COUNTROWS(FILTER(Table2, Table2[technology_score] >= 1))
VAR total_svc = COUNTROWS(FILTER(Table2, Table2[service_experience_score] >= 1))
VAR total_fuel = COUNTROWS(FILTER(Table2, Table2[fuel_or_range_score] >= 1))
VAR total_perf = COUNTROWS(FILTER(Table2, Table2[performance_score] >= 1))
VAR neg_maint = COUNTROWS(FILTER(Table2, Table2[maintenance_score] IN {1,2}))
VAR neg_comf = COUNTROWS(FILTER(Table2, Table2[comfort_score] IN {1,2}))
VAR neg_tech = COUNTROWS(FILTER(Table2, Table2[technology_score] IN {1,2}))
VAR neg_svc = COUNTROWS(FILTER(Table2, Table2[service_experience_score] IN {1,2}))
VAR neg_fuel = COUNTROWS(FILTER(Table2, Table2[fuel_or_range_score] IN {1,2}))
VAR neg_perf = COUNTROWS(FILTER(Table2, Table2[performance_score] IN {1,2}))
RETURN
SWITCH(asp,
    "Maintenance", DIVIDE(neg_maint, total_maint) * 100,
    "Comfort", DIVIDE(neg_comf, total_comf) * 100,
    "Technology", DIVIDE(neg_tech, total_tech) * 100,
    "Service", DIVIDE(neg_svc, total_svc) * 100,
    "Fuel/Range", DIVIDE(neg_fuel, total_fuel) * 100,
    "Performance", DIVIDE(neg_perf, total_perf) * 100
)
```

### Neutral %
```dax
Neutral % = 
VAR asp = SELECTEDVALUE(Aspects[Aspect])
VAR total_maint = COUNTROWS(FILTER(Table2, Table2[maintenance_score] >= 1))
VAR total_comf = COUNTROWS(FILTER(Table2, Table2[comfort_score] >= 1))
VAR total_tech = COUNTROWS(FILTER(Table2, Table2[technology_score] >= 1))
VAR total_svc = COUNTROWS(FILTER(Table2, Table2[service_experience_score] >= 1))
VAR total_fuel = COUNTROWS(FILTER(Table2, Table2[fuel_or_range_score] >= 1))
VAR total_perf = COUNTROWS(FILTER(Table2, Table2[performance_score] >= 1))
VAR neu_maint = COUNTROWS(FILTER(Table2, Table2[maintenance_score] = 3))
VAR neu_comf = COUNTROWS(FILTER(Table2, Table2[comfort_score] = 3))
VAR neu_tech = COUNTROWS(FILTER(Table2, Table2[technology_score] = 3))
VAR neu_svc = COUNTROWS(FILTER(Table2, Table2[service_experience_score] = 3))
VAR neu_fuel = COUNTROWS(FILTER(Table2, Table2[fuel_or_range_score] = 3))
VAR neu_perf = COUNTROWS(FILTER(Table2, Table2[performance_score] = 3))
RETURN
SWITCH(asp,
    "Maintenance", DIVIDE(neu_maint, total_maint) * 100,
    "Comfort", DIVIDE(neu_comf, total_comf) * 100,
    "Technology", DIVIDE(neu_tech, total_tech) * 100,
    "Service", DIVIDE(neu_svc, total_svc) * 100,
    "Fuel/Range", DIVIDE(neu_fuel, total_fuel) * 100,
    "Performance", DIVIDE(neu_perf, total_perf) * 100
)
```

### Positive %
```dax
Positive % = 
VAR asp = SELECTEDVALUE(Aspects[Aspect])
VAR total_maint = COUNTROWS(FILTER(Table2, Table2[maintenance_score] >= 1))
VAR total_comf = COUNTROWS(FILTER(Table2, Table2[comfort_score] >= 1))
VAR total_tech = COUNTROWS(FILTER(Table2, Table2[technology_score] >= 1))
VAR total_svc = COUNTROWS(FILTER(Table2, Table2[service_experience_score] >= 1))
VAR total_fuel = COUNTROWS(FILTER(Table2, Table2[fuel_or_range_score] >= 1))
VAR total_perf = COUNTROWS(FILTER(Table2, Table2[performance_score] >= 1))
VAR pos_maint = COUNTROWS(FILTER(Table2, Table2[maintenance_score] IN {4,5}))
VAR pos_comf = COUNTROWS(FILTER(Table2, Table2[comfort_score] IN {4,5}))
VAR pos_tech = COUNTROWS(FILTER(Table2, Table2[technology_score] IN {4,5}))
VAR pos_svc = COUNTROWS(FILTER(Table2, Table2[service_experience_score] IN {4,5}))
VAR pos_fuel = COUNTROWS(FILTER(Table2, Table2[fuel_or_range_score] IN {4,5}))
VAR pos_perf = COUNTROWS(FILTER(Table2, Table2[performance_score] IN {4,5}))
RETURN
SWITCH(asp,
    "Maintenance", DIVIDE(pos_maint, total_maint) * 100,
    "Comfort", DIVIDE(pos_comf, total_comf) * 100,
    "Technology", DIVIDE(pos_tech, total_tech) * 100,
    "Service", DIVIDE(pos_svc, total_svc) * 100,
    "Fuel/Range", DIVIDE(pos_fuel, total_fuel) * 100,
    "Performance", DIVIDE(pos_perf, total_perf) * 100
)
```

---

## Delivery Satisfaction (Disconnected Delivery_Buckets Table)

### Delivery_Buckets Table (Enter Data — no relationship)
| Bucket | Sort | Min_Days | Max_Days |
|--------|------|----------|----------|
| 3-5d | 1 | 3 | 5 |
| 6-7d | 2 | 6 | 7 |
| 8-10d | 3 | 8 | 10 |
| 11-13d | 4 | 11 | 13 |
| 14-16d | 5 | 14 | 16 |
| 17-20d | 6 | 17 | 20 |
| 21-25d | 7 | 21 | 25 |
| 25+d | 8 | 26 | 100 |

### Delivery Satisfaction %
```dax
Delivery Satisfaction % = 
VAR minD = SELECTEDVALUE(Delivery_Buckets[Min_Days])
VAR maxD = SELECTEDVALUE(Delivery_Buckets[Max_Days])
VAR total = COUNTROWS(FILTER(Table2, Table2[Delivery_Days] >= minD && Table2[Delivery_Days] <= maxD))
VAR satisfied = COUNTROWS(FILTER(Table2, Table2[Delivery_Days] >= minD && Table2[Delivery_Days] <= maxD && Table2[Sentiment_Label] = "Satisfied"))
RETURN
IF(total > 0, DIVIDE(satisfied, total) * 100, 0)
```

---

## Service Satisfaction (Disconnected Service_Buckets Table)

### Service_Buckets Table (Enter Data — no relationship)
| Bucket | Sort | Min_Svc | Max_Svc |
|--------|------|---------|---------|
| 0-1 visits | 1 | 0 | 0.99 |
| 1-2 visits | 2 | 1 | 1.99 |
| 2-3 visits | 3 | 2 | 2.99 |
| 3-4 visits | 4 | 3 | 3.99 |
| 4-5 visits | 5 | 4 | 4.99 |
| 5+ visits | 6 | 5 | 100 |

### Service Satisfaction %
```dax
Service Satisfaction % = 
VAR minS = SELECTEDVALUE(Service_Buckets[Min_Svc])
VAR maxS = SELECTEDVALUE(Service_Buckets[Max_Svc])
VAR total = COUNTROWS(FILTER(Table2, Table2[Service_History] >= minS && Table2[Service_History] <= maxS))
VAR satisfied = COUNTROWS(FILTER(Table2, Table2[Service_History] >= minS && Table2[Service_History] <= maxS && Table2[Sentiment_Label] = "Satisfied"))
RETURN
IF(total > 0, DIVIDE(satisfied, total) * 100, 0)
```

---

## Tooltip Measure

### Total Mentioned Reviews
```dax
Total Mentioned Reviews = 
VAR asp = SELECTEDVALUE(Aspects[Aspect])
RETURN
SWITCH(asp,
    "Maintenance", COUNTROWS(FILTER(Table2, Table2[maintenance_score] >= 1)),
    "Comfort", COUNTROWS(FILTER(Table2, Table2[comfort_score] >= 1)),
    "Technology", COUNTROWS(FILTER(Table2, Table2[technology_score] >= 1)),
    "Service", COUNTROWS(FILTER(Table2, Table2[service_experience_score] >= 1)),
    "Fuel/Range", COUNTROWS(FILTER(Table2, Table2[fuel_or_range_score] >= 1)),
    "Performance", COUNTROWS(FILTER(Table2, Table2[performance_score] >= 1))
)
```
