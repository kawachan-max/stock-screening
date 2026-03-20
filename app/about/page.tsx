import Link from "next/link";

const PAGE_TITLE = "\u3053\u306e\u30b9\u30af\u30ea\u30fc\u30cb\u30f3\u30b0\u30b5\u30fc\u30d3\u30b9\u306b\u3064\u3044\u3066";
const BACK_LINK = "\u2190 \u30e9\u30f3\u30ad\u30f3\u30b0\u306b\u623b\u308b";

const CATCH_1 = "\u3082\u30571998\u5e74\u3001\u3042\u306a\u305f\u304c\u30e6\u30cb\u30af\u30ed\u682a\u3092\u6301\u3063\u3066\u3044\u305f\u3089\u3002";
const CATCH_2 = "\u4eca\u9803\u3001\u6295\u8cc7\u984d\u306f900\u500d\u306b\u306a\u3063\u3066\u3044\u305f\u3002";
const CATCH_3 = "100\u4e07\u5186\u304c\u2014\u20149\u5104\u5186\u306b\u3002";
const CATCH_4 = "\u30cb\u30c8\u30ea\u3082\u540c\u3058\u3067\u3059\u3002\u4e0a\u5834\u5f53\u6642\u306e\u682a\u4fa1\u306f\u4eca\u306e300\u5206\u306e\u0031\u3002";
const CATCH_5 = "\u306a\u305c\u304b\uff1f\u3000\u5c0f\u3055\u3059\u304e\u3066\u3001\u8ab0\u3082\u898b\u3066\u3044\u306a\u304b\u3063\u305f\u304b\u3089\u3002";
const CATCH_6 = "\u6b21\u306e\u30e6\u30cb\u30af\u30ed\u306f\u3001\u4eca\u3053\u306e\u77ac\u9593\u3082\u6771\u8a3c\u306e\u3069\u3053\u304b\u306b\u3044\u308b\u3002";
const CATCH_7 = "\u6642\u4fa1\u7dcf\u984d30\uff5e500\u5104\u5186\u3002\u6a5f\u95a2\u6295\u8cc7\u5bb6\u304c\u624b\u3092\u51fa\u305b\u306a\u3044\u30b5\u30a4\u30ba\u3002\u3060\u304b\u3089\u5272\u5b89\u306a\u307e\u307e\u653e\u7f6e\u3055\u308c\u3066\u3044\u308b\u3002";
const CATCH_8 = "\u3053\u306e\u30b5\u30fc\u30d3\u30b9\u306f\u3001\u305d\u306e\u300c\u307e\u3060\u8ab0\u3082\u6c17\u3065\u3044\u3066\u3044\u306a\u3044\u9298\u67c4\u300d\u3092\u2014\u2014\u4f1d\u8aac\u306e\u6295\u8cc7\u5bb62\u4eba\u306e\u624b\u6cd5\u3068AI\u3092\u4f7f\u3063\u3066\u3001\u6bce\u55b6\u696d\u65e5\u30b9\u30af\u30ea\u30fc\u30cb\u30f3\u30b0\u3057\u307e\u3059\u3002";
const FEATURE_TITLE = "\u3053\u306e\u30b5\u30fc\u30d3\u30b9\u3067\u3067\u304d\u308b\u3053\u3068";
const FEATURE_1 = "\u6bce\u55b6\u696d\u65e5\u3001\u6771\u8a3c3\uff0c300\u9298\u67c4\u3092\u81ea\u52d5\u30b9\u30af\u30ea\u30fc\u30cb\u30f3\u30b0";
const FEATURE_2 = "\u5272\u5b89\u5ea6\u00d7\u6210\u9577\u6027\u00d7\u682a\u4e3b\u9084\u5143\u3092\u30b9\u30b3\u30a2\u5316\u3057\u3066\u9806\u4f4d\u4ed8\u3051";
const FEATURE_3 = "AI\u304c\u6c7a\u7b97\u66f8\u3092\u8aad\u3093\u3067\u3001\u696d\u7e3e\u30c8\u30ec\u30f3\u30c9\u3092\u89e3\u8aac";
const HOWTO_TITLE = "\u30e9\u30f3\u30ad\u30f3\u30b0\u306e\u898b\u65b9";
const HOWTO_SCORE = "\u30b9\u30b3\u30a2\uff08100\u70b9\u6e80\u70b9\uff09";
const HOWTO_SCORE_DESC = "\u5272\u5b89\u5ea6\u30fb\u6210\u9577\u6027\u30fb\u682a\u4e3b\u9084\u5143\u4f59\u5730\u30fb\u30ea\u30b9\u30af\u6e1b\u70b9\u306e\u5408\u8a08\u3002\u9ad8\u3044\u307b\u3069\u5272\u5b89\u304b\u3064\u512a\u826f\u306a\u9298\u67c4";
const HOWTO_BADGE = "\u8a55\u4fa1\u30d0\u30c3\u30b8\uff08\u25ce\u25cb\u25b3\u00d7\uff09";
const HOWTO_BADGE_DESC = "\u5404\u9805\u76ee\u306e\u5272\u5b89\u5ea6\u30fb\u6210\u9577\u6027\u3092\u76f4\u611f\u7684\u306b\u8868\u793a\u3002\u25ce\uff1d\u512a\u79c0\u3001\u00d7\uff1d\u8981\u6ce8\u610f";
const HOWTO_LOCK = "\u30ed\u30c3\u30af\u89e3\u9664";
const HOWTO_LOCK_DESC = "1\uff5e10\u4f4d\u306f\u6709\u6599\u30d7\u30e9\u30f3\u3067\u89e3\u653e\u3002note\u8a18\u4e8b\uff08\uffe51\uff0c980\uff09\u306e\u30d1\u30b9\u30ef\u30fc\u30c9\u3092\u5165\u529b";
const CONDITION_TITLE = "\ud83d\udccb \u30b9\u30af\u30ea\u30fc\u30cb\u30f3\u30b0\u6761\u4ef6";
const BADGE_MARKET_CAP = "\u6642\u4fa1\u7dcf\u984d 30\u301c500\u5104\u5186";
const BADGE_PER = "PER 10\u500d\u4ee5\u4e0b";
const BADGE_NC = "NC\u6bd4\u7387 1.0\u4ee5\u4e0a";
const BADGE_PROFIT = "\u9ed2\u5b57\u4f01\u696d\u306e\u307f";
const BADGE_EXCLUDE = "\u91d1\u878d\u30fb\u4e0d\u52d5\u7523\u9664\u5916";
const DIFF_TITLE = "\u306a\u305c\u3053\u306e\u30b5\u30fc\u30d3\u30b9\u306f\u4ed6\u3068\u9055\u3046\u306e\u304b\uff1f";
const DIFF_QUOTE = "\u300c\u4e2d\u8eab\u306e\u308f\u304b\u3089\u306a\u3044\u3082\u306e\u306b\u306f\u6295\u8cc7\u3057\u306a\u3044\u300d\u2014 \u30a6\u30a9\u30fc\u30ec\u30f3\u30fb\u30d0\u30d5\u30a7\u30c3\u30c8";
const DIFF_BODY1 = "\u30a4\u30f3\u30d5\u30eb\u30a8\u30f3\u30b5\u30fc\u306e\u6839\u62e0\u306e\u306a\u3044\u9298\u67c4\u63a8\u5968\u3084\u3001\u4e2d\u8eab\u306e\u308f\u304b\u3089\u306a\u3044\u8a3c\u5238\u4f1a\u793e\u304c\u63d0\u6848\u3059\u308b\u30d5\u30a1\u30f3\u30c9\u30fb\u4ed5\u7d44\u307f\u50b5\u306b\u8e0a\u3089\u3055\u308c\u3066\u3044\u307e\u305b\u3093\u304b\uff1f";
const DIFF_BODY2 = "\u3053\u306e\u30b5\u30fc\u30d3\u30b9\u306f\u30012\u4eba\u306e\u5049\u5927\u306a\u6295\u8cc7\u5bb6\u306e\u6295\u8cc7\u6cd5\u3092\u3082\u3068\u306b\u3001\u3059\u3079\u3066\u306e\u6839\u62e0\u3092\u30b9\u30b3\u30a2\u3067\u898b\u3048\u308b\u5316\u3057\u3066\u3044\u307e\u3059\u3002";
const DIFF_BODY3 = "\u3042\u306a\u305f\u81ea\u8eab\u304c\u9298\u67c4\u3092\u898b\u6975\u3081\u308b\u76ee\u3092\u990a\u3044\u306a\u304c\u3089\u7b2c\u4e8c\u306e\u30e6\u30cb\u30af\u30ed\u3001\u7b2c\u4e8c\u306e\u30cb\u30c8\u30ea\u3092\u8ab0\u3088\u308a\u3082\u65e9\u304f\u898b\u3064\u3051\u308b\u3053\u3068\u304c\u3067\u304d\u308b\u3002\u305d\u308c\u304c\u3053\u306e\u30b5\u30fc\u30d3\u30b9\u306e\u672c\u8cea\u3067\u3059\u3002";
const PITCH_DESCRIPTION = "\u500b\u4eba\u8cc7\u7523900\u5104\u5186\u8d85\u306e\u4f1d\u8aac\u306e\u6295\u8cc7\u5bb6\u30fb\u6e05\u539f\u9054\u90ce\u306e\u6295\u8cc7\u6cd5\u3068\u3001\u500b\u4eba\u8cc7\u7523\u7d0424\u5146\u5186\u30fb\u6295\u8cc7\u306e\u795e\u69d8\u30a6\u30a9\u30fc\u30ec\u30f3\u30fb\u30d0\u30d5\u30a7\u30c3\u30c8\u306e\u30cf\u30a4\u30d6\u30ea\u30c3\u30c9\u300c\u30cd\u30c3\u30c8\u30ad\u30e3\u30c3\u30b7\u30e5\u6bd4\u7387\u00d7\u30d0\u30ea\u30e5\u30fc\u6295\u8cc7\u300d\u306b\u6c7a\u7b97\u66f8\u3092\u8aad\u307f\u8fbc\u307e\u305b\u30b9\u30b3\u30a2\u30ea\u30f3\u30b0\u3057\u305f\u552f\u4e00\u7121\u4e8c\u306e\u30b9\u30af\u30ea\u30fc\u30cb\u30f3\u30b0\u30b5\u30fc\u30d3\u30b9";

const DISCLAIMER_TITLE = "\u514d\u8cac\u4e8b\u9805";
const DISCLAIMER_1 = "\u672c\u30b5\u30fc\u30d3\u30b9\u306f\u60c5\u5831\u63d0\u4f9b\u3092\u76ee\u7684\u3068\u3057\u305f\u3082\u306e\u3067\u3042\u308a\u3001\u6295\u8cc7\u52a9\u8a00\u30fb\u9298\u67c4\u63a8\u5968\u3092\u884c\u3046\u3082\u306e\u3067\u306f\u3042\u308a\u307e\u305b\u3093\u3002";
const DISCLAIMER_2 = "\u8868\u793a\u3055\u308c\u308b\u30b9\u30b3\u30a2\u30fb\u30e9\u30f3\u30ad\u30f3\u30b0\u306f\u30a2\u30eb\u30b4\u30ea\u30ba\u30e0\u304a\u3088\u3073AI\u306b\u3088\u308b\u5206\u6790\u306b\u57fa\u3065\u304f\u3082\u306e\u3067\u3059\u3002\u5c06\u6765\u306e\u682a\u4fa1\u5909\u52d5\u3084\u6295\u8cc7\u6210\u679c\u3092\u4fdd\u8a3c\u3059\u308b\u3082\u306e\u3067\u306f\u3042\u308a\u307e\u305b\u3093\u3002";
const DISCLAIMER_3 = "\u6295\u8cc7\u306b\u306f\u5e38\u306b\u30ea\u30b9\u30af\u304c\u4f34\u3044\u307e\u3059\u3002\u5143\u672c\u640d\u5931\u306e\u53ef\u80fd\u6027\u304c\u3042\u308a\u3001\u6295\u8cc7\u5224\u65ad\u306f\u5fc5\u305a\u3054\u81ea\u8eab\u306e\u8cac\u4efb\u3067\u884c\u3063\u3066\u304f\u3060\u3055\u3044\u3002";
const DISCLAIMER_4 = "\u30b9\u30b3\u30a2\u30ea\u30f3\u30b0\u306b\u306f\u30d0\u30d5\u30a7\u30c3\u30c8\u6c0f\u30fb\u6e05\u539f\u9054\u90ce\u6c0f\u306e\u516c\u958b\u60c5\u5831\u306b\u57fa\u3065\u304f\u6295\u8cc7\u54f2\u5b66\u3092\u53c2\u8003\u306b\u3057\u3066\u3044\u307e\u3059\u304c\u3001\u4e21\u6c0f\u3068\u306f\u7121\u95a2\u4fc2\u3067\u3059\u3002";
const DISCLAIMER_5 = "\u30c7\u30fc\u30bf\u306fyfinance\u304a\u3088\u3073JPX\u516c\u5f0f\u60c5\u5831\u3092\u5229\u7528\u3057\u3066\u304a\u308a\u3001\u6700\u65b0\u60c5\u5831\u3068\u7570\u306a\u308b\u5834\u5408\u304c\u3042\u308a\u307e\u3059\u3002\u5fc5\u305a\u516c\u5f0f\u60c5\u5831\u3067\u3054\u78ba\u8a8d\u304f\u3060\u3055\u3044\u3002";

const BADGES = [BADGE_MARKET_CAP, BADGE_PER, BADGE_NC, BADGE_PROFIT, BADGE_EXCLUDE];

export default function AboutPage() {
  return (
    <div className="min-h-screen bg-[#f9f7f4] text-[#1a1a1a]">
      <div className="max-w-2xl mx-auto px-4 py-8">
        <Link
          href="/"
          className="inline-block text-sm text-[#6b6b6b] underline hover:text-[#4a4a4a] mb-6"
        >
          {BACK_LINK}
        </Link>

        <h1 className="text-xl font-bold text-[#1a1a1a] mb-8">{PAGE_TITLE}</h1>

        <div className="rounded-xl border border-[#f59e0b] bg-[#fffbeb] p-6 text-base leading-relaxed">
          <section className="mb-6">
            <p className="text-xl font-bold text-gray-800 mb-2">{CATCH_1}</p>
            <p className="text-3xl font-black text-amber-600 mb-1">{CATCH_2}</p>
            <p className="text-lg text-gray-600 italic mb-4">{CATCH_3}</p>
            <p className="text-base text-gray-700 mb-1">{CATCH_4}</p>
            <p className="text-sm text-gray-500 italic mb-6">{CATCH_5}</p>
            <hr className="border-[#f59e0b]/50 my-4" />
            <p className="text-lg font-bold text-gray-800 mb-2">{CATCH_6}</p>
            <p className="text-sm text-gray-600 mb-2">{CATCH_7}</p>
            <p className="text-sm text-gray-700 mb-6">{CATCH_8}</p>
            <hr className="border-[#f59e0b]/50 my-4" />
          </section>
          <section className="bg-white rounded-lg p-4 mb-6">
            <h2 className="text-sm font-bold text-gray-500 mb-3">{FEATURE_TITLE}</h2>
            <p className="text-sm text-gray-700">{"\u2705 "}{FEATURE_1}</p>
            <p className="text-sm text-gray-700">{"\u2705 "}{FEATURE_2}</p>
            <p className="text-sm text-gray-700">{"\u2705 "}{FEATURE_3}</p>
          </section>
          <section className="bg-white rounded-lg p-4 mb-6">
            <h2 className="text-sm font-bold text-gray-500 mb-3">{HOWTO_TITLE}</h2>
            <p className="mb-1.5">
              <span className="font-bold">{"\uD83D\uDCCA "}{HOWTO_SCORE}</span>
              <span className="block text-xs text-gray-500">{HOWTO_SCORE_DESC}</span>
            </p>
            <p className="mb-1.5">
              <span className="font-bold">{"\uD83C\uDFC5 "}{HOWTO_BADGE}</span>
              <span className="block text-xs text-gray-500">{HOWTO_BADGE_DESC}</span>
            </p>
            <p>
              <span className="font-bold">{"\uD83D\uDD12 "}{HOWTO_LOCK}</span>
              <span className="block text-xs text-gray-500">{HOWTO_LOCK_DESC}</span>
            </p>
          </section>
          <section className="mb-6">
            <h2 className="text-sm font-bold text-gray-500 mb-3">{CONDITION_TITLE}</h2>
            <div className="flex flex-wrap gap-2">
              {BADGES.map((label) => (
                <span
                  key={label}
                  className="px-2.5 py-1 rounded-md bg-[#f0ece6] text-[#4a4a4a] text-sm"
                >
                  {label}
                </span>
              ))}
            </div>
          </section>
          <section className="mb-6">
            <h2 className="text-base font-bold text-gray-800 mb-3">{DIFF_TITLE}</h2>
            <blockquote className="pl-4 py-2 my-3 rounded-lg bg-white/80 text-gray-700 text-base border-l-4 border-amber-500">
              {DIFF_QUOTE}
            </blockquote>
            <ul className="list-disc list-inside space-y-2 text-gray-700">
              <li>{DIFF_BODY1}</li>
              <li>{DIFF_BODY2}</li>
              <li>{DIFF_BODY3}</li>
            </ul>
          </section>
          <section>
            <p className="text-gray-700 leading-relaxed">{PITCH_DESCRIPTION}</p>
          </section>
        </div>

        <div className="bg-[#f5f0e8] rounded-xl p-6 mt-12">
          <h2 className="text-sm font-bold text-[#4a4a4a] mb-3">{DISCLAIMER_TITLE}</h2>
          <p className="text-xs text-[#6b6b6b] leading-relaxed mb-2">{"\u30FB "}{DISCLAIMER_1}</p>
          <p className="text-xs text-[#6b6b6b] leading-relaxed mb-2">{"\u30FB "}{DISCLAIMER_2}</p>
          <p className="text-xs text-[#6b6b6b] leading-relaxed mb-2">{"\u30FB "}{DISCLAIMER_3}</p>
          <p className="text-xs text-[#6b6b6b] leading-relaxed mb-2">{"\u30FB "}{DISCLAIMER_4}</p>
          <p className="text-xs text-[#6b6b6b] leading-relaxed mb-2">{"\u30FB "}{DISCLAIMER_5}</p>
        </div>
      </div>
    </div>
  );
}



