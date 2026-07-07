# الند AlNedd

الند نظام تشغيل أعمال محلي مبسط: registry للوحدات، dashboard لحالتها، وتحويل رسائل/أحداث إلى work orders موجهة للوحدة المناسبة.

## آلية العمل

1. `init` ينشئ registry للوحدات المحلية.
2. `dashboard` يفحص وجود الوحدات ومساراتها.
3. `order` يحول رسالة إلى work order.
4. `convert-bitext` يحول بيانات Bitext إلى أحداث.
5. `batch/stress` يقيسان توزيع الأوامر والانهيار.

## تشغيل سريع

```powershell
python -m alnedd.cli init
python -m alnedd.cli dashboard
python -m alnedd.cli order --message "refund customer"
```

## بيانات الاختبار

تعتمد على 12,000 رسالة Bitext التي جلبها `C:\Projects\almandoub` من الإنترنت.

## آخر نتائج

- الاختبارات الذاتية: 2/2 ناجحة.
- Registry افتراضي: 4 وحدات محلية.
- Benchmark: 12,000 work orders، errors=0، p99=0.013ms.
- توزيع الملاك: almandoub=2,315، alkhaliya=9,635، alharis_alsahabi=50.
- Stress: 36,000 work orders، errors=0، p99=0.012ms، peak memory=1.18MB.

## تحسينات إنتاجية 2026-07-04

- registry يربط كل وحدة بمسار ودور، وdashboard يكشف الوحدات المفقودة.
- work_order يعطي owner/status/kind موحداً بدلاً من نص عشوائي.
- batch/stress يقيسان توزيع العمل بين الوحدات لا الأخطاء فقط.

## التشغيل المؤسسي (Enterprise) — v1.0.0

- **خدمة control plane عبر HTTP**: `python -m alnedd.cli serve` → `GET /api/dashboard` (صحة الوحدات) و`POST /api/order {"message"}` (توجيه أوامر العمل).
- **نقاط فحص**: `/api/health` (مفتوح) · `/api/version` · `/api/metrics`.
- **تهيئة عبر البيئة**: متغيرات `ALNEDD_*` (منها `ALNEDD_REGISTRY`) — انظر `docs/OPERATIONS.md`.
- **مصادقة**: `ALNEDD_API_KEY` → ترويسة `X-API-Key`. **سجلات JSON**: `logs\alnedd.service.jsonl`.
