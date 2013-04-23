# coding=utf-8
from model import *

def create_test_data():
    alon = User(u"אלון", "")
    anat = User(u"ענת", "")
    tomer = User(u"תומר", "")

    relationship = Conversation(anat, u'אני מפחדת להרוס את היחסים')

    Message(relationship, anat, u"אני בטיפול ממושך להבראת דפוסים לא בריאים\nאחרי שבמשך שנים החרבתי מערכות יחסים בזו אחר זו\nולא תכננתי להכנס למערכת היחסים הזו\nואני מאד חרדה להחריב גם אותה\nואני סובלת, ליטרלי\nכאב\nאמיתי")
    Message(relationship, alon, u"מה יחריב את היחסים?")
    Message(relationship, anat, u"שאני אחזור על השגיאות\nשאני לא אצליח בחיים האישיים שלי\nוזה יהפוך אותי לבן אדם שלא ראוי לחיות איתו")
    Message(relationship, alon, u"מה יהפוך אותך לאדם שלא ראוי לחיות איתו?")
    Message(relationship, anat, u"שאני אתקע, שאני לא אתקדם, שאני לא אוכל לתרום במידה שווה\nהקטע הכלכלי מפריע לי באופן מיוחד")
    Message(relationship, alon, u"מה קורה בתחום הכלכלי?")
    Message(relationship, anat, u"דווקא עשיתי קפיצה לא רעה בשנה פלוס האחרונות\nאבל\nאני לא יכולה להגיע לרמות שכר, זה נורא מפגר\nכשאני קוראת את המשפטים של עצמי\nאבל אלהים כמה שזה כואב")
    Message(relationship, alon, u"מה זה אומר בשבילך שאת לא יכולה להגיע לרמות השכר של חבר שלך?")
    Message(relationship, anat, u"שאני לא יכולה לתרום באותה המידה\nליחסים\nלחיים משותפים")
    Message(relationship, alon, u"הוא יודע שאת מקנאה?")
    Message(relationship, anat, u"ברור")
    Message(relationship, alon, u"מגניב!")
    Message(relationship, anat, u"אבל זה לא יוצא עליו בלייב")
    Message(relationship, alon, u"למה לא?")
    Message(relationship, anat, u"למדתי להוציא את זה על אנשים אחרים\nכשאני מרגישה שהמפלצת מרימה את ראשה\nאני פשוט תופסת ממנו מרחק")
    Message(relationship, alon, u"למה את קוראת לזה \"להוציא\"?")
    Message(relationship, anat, u"להגיד מה שאני באמת חושבת ומרגישה\nהוא אף פעם לא רואה אותי מתפרקת, רק אנשים אחרים\nכי ההתפרקויות החריבו יחסים\nבעבר\nאחד הדפוסים")
    Message(relationship, alon, u"אז את מתרחקת")
    Message(relationship, anat, u"נכון")
    Message(relationship, alon, u"בנסיון לשמור על היחסים\nנכון?")
    Message(relationship, anat, u"אמת")
    Message(relationship, alon, u"תקראי את זה רגע שוב")
    Message(relationship, anat, u"קראתי")
    Message(relationship, alon, u"להתרחק בשביל לשמור על היחסים")
    Message(relationship, anat, u"נכון\nכי יש לי הרגשה שאם אני אוציא את הדברים החוצה כמו שהם היחסים לא יחזיקו מעמד\nכמו שהיחסים הקודמים לא החזיקו מעמד")
    Message(relationship, alon, u"סיפרת בשיחה קודמת שהוא התאהב בך כשסיפרת לו את הדברים הכי רעים עלייך")
    Message(relationship, anat, u"נכון\nלא מדויק -\nמה שקרה הוא\nשסיפרתי דברים רעים כי לא רציתי לעמוד בפני הדילמה הזאת\nוזה דווקא מה שקרב בינינו")
    Message(relationship, alon, u"אני רוצה להגיד לך שאת תותחית על חלל\nרק על הקטע הזה שנכנסת בעובי הקורה\nבשתי דקות של שיחה")
    Message(relationship, anat, u"תודה")
    Message(relationship, alon, u"בבקשה\nאוקיי\nאז כשהכרתם, דברים שסיפרת לו שחשבת שירחיקו אותו ממך, גרמו לו להתקרב")
    Message(relationship, anat, u"נכון")
    Message(relationship, alon, u"ומה קורה עכשיו?\nמה שונה עכשיו?")
    Message(relationship, anat, u"זה נעצר\nאני לא יכולה להוציא את מה שנראה בעיני מפלצת")
    Message(relationship, alon, u"אז מה מפלצתי בך?")
    Message(relationship, anat, u"אני קנאית\nיש לי מצבי רוח רעים\nאני לא רוצה להרגיש שאני תופסת את כל המקום\nולא נותנת מקום\nיש לי חרדות המוות מלא להצליח\nיש לי היסטוריה לא מפוארת ודפוסי התנהגות שממש פחיד אותי שהם יחזרו\nנראה לי שסיכמתי")
    Message(relationship, alon, u"מה הכי נורא מכל אלה?")
    Message(relationship, anat, u"שאלה טובה\nקשה לי להגיד\nאולי הקנאה,\nהיא לא הכי נוראה\nאבל היא הכי מכאיבה\nוכשהיא מכאיבה\nאני יודעת שהיא לא הגיונית\nאבל היא ממש מכאיבה לי")
    Message(relationship, alon, u"מה את הכי מפחדת שהוא ידע?")
    Message(relationship, anat, u"איך הקנאה שלי נראית")
    Message(relationship, alon, u"ואיך היא נראית?")
    Message(relationship, anat, u"רע")
    Message(relationship, alon, u"ספרי לי")
    Message(relationship, anat, u"אני שונאת אותן")
    Message(relationship, alon, u"אותן?")
    Message(relationship, anat, u"כן")
    Message(relationship, alon, u"נשים אחרות?")
    Message(relationship, anat, u"כן")
    Message(relationship, alon, u"יש מישהי ספציפית?")
    Message(relationship, anat, u"לא\nיש הרבה")
    Message(relationship, alon, u"הרבה ספציפיות, או כל בחורה שמסתכלת עליו?")
    Message(relationship, anat, u"הרבה ספציפיות")
    Message(relationship, alon, u"הקנאה זה מה שהרס את היחסים הקודמים שלך?")
    Message(relationship, anat, u"ממש לא\nאבל הכעס\nוהדרך שביטאתי אותו\nכן")
    Message(relationship, alon, u"ועל מה כעסת?")
    Message(relationship, anat, u"וואו\nעל מיליון דברים")
    Message(relationship, alon, u"מה הדבר הראשון שקופץ לך לראש?")
    Message(relationship, anat, u"*****\nשתמות\nזה פשוט גם גילוי של קנאה")
    Message(relationship, alon, u"על מה כעסת עליה?")
    Message(relationship, anat, u"שהיא באה ונכנסה לי לחיים\nודרסה אותי בניסיון להשיג את מה שהיא רצתה\nשהיא נכנסה לטריטוריה שלי, לבית שלי\nודרכה עלי")
    Message(relationship, alon, u"אני רוצה לשמוע יותר על *****\nמה בדיוק היא עשתה\nומה בדיוק הרגשת")
    Message(relationship, anat, u"טוב\nזה נחלק לשני חלקים\nהחלק הראשון הוא כשעוד הייתי עם *****\nנכנסתי הביתה ותפסתי אותם על חם כמו בסרטים\nהפרעתי להם באמצע\nוהחלק השני היה\nשהוא הלך אליה וגר אצלה\nשזה כבר לא כעס עליה אלא עליו\nזה כבר לא מזיז לי היום")
    Message(relationship, alon, u"ובפעם הראשונה לא כעסת עליו?")
    Message(relationship, anat, u"לא")
    Message(relationship, alon, u"רק עליה?")
    Message(relationship, anat, u"כן\nרק עליה")
    Message(relationship, alon, u"לא ראית בו אחראי?")
    Message(relationship, anat, u"לא\nממש ככה")
    Message(relationship, alon, u"לא ראית אותו ממטר")
    Message(relationship, anat, u"דווקא ראיתי\nאחרי זה, בפעם השניה\nראיתי אותו גם")
    Message(relationship, alon, u"ומה קורה לך במערכת היחסים הנוכחית?\nתפסת את ***** עם מישהי?")
    Message(relationship, anat, u"ממש לא\nאני מרגישה בעיקר כאב\nבכל מיני סיטואציות\nכאב פיזי ממש")
    Message(relationship, alon, u"איפה?")
    Message(relationship, anat, u"איפה בגוף?")
    Message(relationship, alon, u"כן")
    Message(relationship, anat, u"בבטן, בחזה\nכשאני רואה כל מיני דברים או עדה לכל מיני דברים")
    Message(relationship, alon, u"מה את רואה שמקפיץ לך את הכאב?")
    Message(relationship, anat, u"אז הדוגמה העיקרית היא *****\nואיך שהיא מתנהגת\nמהיום שהכרנו בערך\nמה שמקפיץ לי...\nשהיא מזמינה אותו לארוחות ערב לבד\nשהיא אומרת לי שהיא פספסה הזדמנות לאהבה אמיתית שהיתה \"כמעט\"\nשהיא מסרבת פאקינג ללכת\nוחייבת להשאר בתמונה כל הזמן\nאבל זה לא רק היא\nזה גם כל מיני אקסיות שעושות \"לייקים\" לתמונות\nכוס אמא של העידן המודרני")
    Message(relationship, alon, u"\nאז את רוצה את ***** רק לעצמך?")
    Message(relationship, anat, u"כן ולא\nבן אדם \"טוב\" תמיד ימשוך תשומת לב חיובית\nזה בא עם החבילה\nזה החלק ההגיוני\nאני פשוט לא יודעת להתמודד עם זה")
    Message(relationship, alon, u"את רוצה שזה לא יגרום לך כאב?")
    Message(relationship, anat, u"בדיוק")
    Message(relationship, alon, u"למה?")
    Message(relationship, anat, u"כי אני סובלת\nואני רוצה להפסיק לסבול")
    Message(relationship, alon, u"האם את סובלת בגלל שכואב, או שאת סובלת בגלל שאת לא רוצה שיכאב?\nאת מבינה את הכוונה שלי?")
    Message(relationship, anat, u"לא")
    Message(relationship, alon, u"אוקיי\nנניח שיש חייל\nוהוא נפצע\nוהוא שוכב בבית החולים\nוכואב לו נורא\nבפצעים\nאבל בנוסף לכל זה\nהוא חושב שהוא בכלל לא היה אמור להפצע\nאם הוא רק היה מתקופף")
    Message(relationship, anat, u"כן, מבינה")
    Message(relationship, alon, u"אז השאלה היא האם הבעיה היא הכאב, או המחשבה שמתלווה אליו?")
    Message(relationship, anat, u"לא. זה הכאב.\nיש עוד משהו\nעכשיו כשאני חושבת על זה\nתמיד חשבתי על שני הדברים אבל אף פעם לא קישרתי\nמאד מפריע לי שבעולם \"הוירטואלי\"\nאף אחד לא יודע מי אני\nואני מרגישה שזה לא לגיטימי לבוא ולדרוש שזה יהיה אחרת\nואני מרגישה שזה לא לגיטימי שאני אגיד את זה אפילו\nאבל\nמי שמכיר את ***** בעולם הוירטואלי לא מכיר אותי\nוזה הולך ביחד")
    Message(relationship, alon, u"אני לא בטוח שהבנתי מה הבנת\nמה הבנת?")
    Message(relationship, anat, u"שזה לא רק הן\nזה גם דברים בדרך שלו שמפריעים לי\nואני לא מסוגלת אפילו להגיד את זה\nכי רק מלקרוא את השורות שאני כותבת עכשיו\nזה נראה לי לא לגיטימי")
    Message(relationship, alon, u"זה נורא כיף לראות אותך עובדת\nומתעמקת\nומחפשת")
    Message(relationship, anat, u"כן. ועכשיו כואבת לי הבטן. והחזה. והלב.\nמהדברים הדבילים האלה")
    Message(relationship, alon, u"או\nרגע\nעצרי\nלמה אלה דברים דביליים?\nאלה הרגשות שלך")
    Message(relationship, anat, u"נכון")
    Message(relationship, alon, u"אוקיי\nאז הרגשות שלך דביליות?\nבואי נסתכל על משהו רגע\nמה הדבר שהכי מפחיד אותך להגיד ל*****?")
    Message(relationship, anat, u"קשה לי להצביע על משפט אחד\nבערך כל מה שאמרתי לך עכשיו")
    Message(relationship, alon, u"ובכל זאת\nמה הדבר שהחשיפה שלו מעוררת הכי הרבה כאב?")
    Message(relationship, anat, u"אולי זה הדבר שהכי מפחיד אותי להגיד\nשההתנהגות החשאית הזאת של *****\nמזמינה את זה\nמזמינה אותן\nודבר שני\nאני רוצה שיתגאו בי")
    Message(relationship, alon, u"למה חשוב לך ש***** יתגאה בך?")
    Message(relationship, anat, u"אררר\nשאלה קשה\nאני מניחה שזה חוזר למה שדיברנו עליו בהתחלה\nלהרגיש בן אדם ראוי\nופה יש גם חלק שהוא שלי")
    Message(relationship, alon, u"אם ***** יתגאה בך, את תרגישי ראויה?\nאו שאם תרגישי ראויה, אז ***** יתגאה בך?")
    Message(relationship, anat, u"שניהם\nאבל ברור שאני צריכה ללמוד להרגיש ראויה ללא קשר")
    Message(relationship, alon, u"איך יראו החיים שלך כשתרגישי לגמרי ראויה?\nמה יקרה?")
    Message(relationship, anat, u"קלילים ונעימים")
    Message(relationship, alon, u"")
    Message(relationship, anat, u"ואני לא אתעצבן מאיזה סתומה שעושה לייק\nאני לא אפחד ואני לא אתרגש מהשטויות האלה")
    Message(relationship, alon, u"אהו!\nנכון\nהפאקצות ימשיכו להציק\n***** ימשיך להסתיר\nואת?")
    Message(relationship, anat, u"זה לא יזיז לי\nכי אני ארגיש כזה בן אדם נפלא\nשאני לא אצטרך את החיזוקים האלה מבחוץ")
    Message(relationship, alon, u"מה שלום הכאב?")
    Message(relationship, anat, u"וואללה\nיש עוד עבודה\nאני יודעת שזה הכיוון")
    Message(relationship, alon, u"מה את יכולה לעשות בכדי להרגיש יותר ראויה?\nמשהו שלא תלוי באף אחד אחר..")
    Message(relationship, anat, u"לא יודעת, זה מעסיק אותי המון\nלא משהו חיצוני כנראה כי דברים דווקא מסתדרים לי מצויין חיצונית\nוזה לא עוזר")
    Message(relationship, alon, u"מה קרה בשיחה הזאת עכשיו?\nמה שיפר את ההרגשה שלך?")
    Message(relationship, anat, u"שדימיינתי את המצב הרצוי")
    Message(relationship, alon, u"אז בואי תקחי את זה צעד אחד קדימה\nתתארי בכתב איך יראו החיים שלך\nכשתרגישי ראויה")
    Message(relationship, anat, u"אוקיי")
    Message(relationship, alon, u"שיעורי בית")
    Message(relationship, anat, u"אחלה\nחפרנו")

    career = Conversation(tomer, u'אני מתלבט אם לקחת אחריות ולהיות מנהל')

    Message(career, tomer, u"אני בהתלבטות מאד קשה, ורוצה קצת שיקופים\nבעקבות הסדנה, בהמלצה של המאמנת, התחלתי קצת לכתוב דברים (ואני לא מתכוון לקוד)\nופתאום שמתי לב שיש לי עניין לא פתור לגבי החלפת התפקיד שלי בעבודה")
    Message(career, alon, u"‫ואללה\n‫מעניין")
    Message(career, tomer, u"ואני מאד מתלבט אם הרצון להחליף תפקיד נובע מרצון אמיתי להתנתק מתפקיד רשמי וניהולי ולהשתחרר מתכנון והערכות זמנים ואחריות, או...\nאו שזה פשוט תירוץ לחשוב שאם רק אחליף תפקיד, הכל יהיה יותר טוב (ומושלם).")
    Message(career, alon, u"‫ומה יצא לך בכתיבה?")
    Message(career, tomer, u"זהו, השאלה עלתה, ועדיין אין תשובה. אבל יש לי הרגשה מאד חזקה שזה לא באמת יעשה שינוי משמעותי.")
    Message(career, alon, u"‫איזה שינוי אתה רוצה שיקרה?")
    Message(career, tomer, u"ובאותה מידה אני יכול להישאר בתפקיד, ולעשות אותו איך שאני חושב שצריך לעשות אותו.\nההיפך: ראיתי המון הערכה על הכנות.")
    Message(career, alon, u"‫אני רוצה לחזור על שאלה שלי - מה אתה רוצה שיקרה?\n‫הרי עשית את הצעד הזה בשביל להשיג משהו, מה זה?")
    Message(career, tomer, u"(חושב)")
    Message(career, alon, u"‫רק אם תדע את התשובה, תוכל לדעת האם הצעד מקרב אותך לשם או לא..")
    Message(career, tomer, u"אני רוצה להרגיש טוב עם מה שאני עושה. אני לא רוצה לעשות דברים בשביל לרצות אף אחד.")
    Message(career, alon, u":)\n‫ואיך זה קשור למציאות בחוץ?")
    Message(career, tomer, u"לא רוצה לרצות את הבוס שלי, ולא את הקולגות שלי.\nואני מספר לעצמי שהם מצפים ממני לעשות דברים באופן מסויים, לא כמו שאני חושב שצריך לעשות.\nובנושא הטכני, יש לי ביטחון עצמי גבוה שאני יודע מה נכון")
    Message(career, alon, u"‫יצא לך לחשוב על איך היית רוצה לעשות את התפקיד בעולם מושלם?")
    Message(career, tomer, u"למרות שהיתה לי תקופה קשה גם בזה, כפי שסיפרתי לך")
    Message(career, alon, u"‫בלי ציפיות מאחרים ובלי רגשות אשם שלך?")
    Message(career, tomer, u"כן! בדיוק.")
    Message(career, alon, u"‫איך זה יראה?")
    Message(career, tomer, u"ובחודשים האחרונים אני מרגיש שאני עושה את התפקיד בצורה הכי טובה עד כה.\nלא עושה ישיבות עם האנשים פעם בשבוע \"כי צריך\"\nלא עושה תכניות עבודה \"כי צריך\"\nפשוט זורם")
    Message(career, alon, u"‫ומה הבעיה עם זה?")
    Message(career, tomer, u"זהו, שגיליתי שאין שום בעיה עם זה.\nלהיפך\nפשוט האמנתי שאני לא מנהל טוב.\nאני זוכר ש*** ב****** התפלא מאד כשאמרתי לי שאני לא חושב שאני מתאים להיות ראש צוות\nהוא אמר שאני אחד הר\"צ הכי טובים שלו\nאמרתי לעצמי שבוא סתם שקרן ורוצה שקט תעשייתי\nואולי הוא לא שיקר")
    Message(career, alon, u"‫מתי הגעת למסקנה שאתה ראש צוות לא טוב?\n‫זה היה לפני ****** אני מניח..")
    Message(career, tomer, u"נראה לי שזה גם שריד מ******.\nשם הייתי פשוט \"לא טוב\".")
    Message(career, alon, u"‫ואו.. הרבה זמן עבר מאז")
    Message(career, tomer, u"הייתי troublemaker")
    Message(career, alon, u"‫וזה בעיניך היום דבר לא טוב?")
    Message(career, tomer, u"ולא שיתפתי פעולה עם אנשים, כי ידעתי איך לעשות הכל \"נכון\" והם לא.\nהיום אני חושב שלהיות troublemaker זה פשוט לא אפקטיבי.\nזה שוחק אותי ואת הסביבה\nולא משיג תוצאות חוץ מתסכול משני הצדדים")
    Message(career, alon, u"‫נכון\n‫ואתה גם לא רוצה להיות כנוע\n‫ולעשות מה שאומרים לך ומה שמצפים ממך")
    Message(career, tomer, u"נכון.")
    Message(career, alon, u"‫והאמת איננה באמצע")
    Message(career, tomer, u"אבל עכשיו אני יכול לראות את הדברים דרך העיניים של אנשים אחרים\nולהבין שאני יכול לעזור להם ולהרגיש טוב\nבלי לרצות אותם")
    Message(career, alon, u"‫ואו!")
    Message(career, tomer, u"זה קרה לי השבוע כמה פעמים בעבודה.")
    Message(career, alon, u"‫זה מטורף מה שאתה אומר\n‫אז רגע")
    Message(career, tomer, u"וההרגשה היתה נפלאה, לעזור כי אני רוצה.")
    Message(career, alon, u"‫מה הבעיה?\n‫אמרת שיש בעיה")
    Message(career, tomer, u"זהו שאין בעיה")
    Message(career, alon, u"‫אני לא רואה בעיה :)")
    Message(career, tomer, u"יש בעיה קטנה")
    Message(career, alon, u"אוקיי..")
    Message(career, tomer, u"שאני חושש שאם אשאר בתפקיד, זה מתוך פחד של מה תהיה האלטרנטיבה\nכמו שהיה כשקיבלתי את התפקיד\nולא מתוך רצון אמיתי\nואת זה אני רוצה לחקור")
    Message(career, alon, u"‫ואתה מנסה להבין מהו רצון אמיתי ומהו פחד?")
    Message(career, tomer, u"בדיוק")
    Message(career, alon, u"‫אוקיי\n‫למה לפעול מתוך פחד זה לא נכון?\n‫זה בהכרח לא נכון?")
    Message(career, tomer, u"*צוחק*")
    Message(career, alon, u":)")
    Message(career, tomer, u"זה נראה לי כמו חולשה")
    Message(career, alon, u"‫אה..\n‫ואתה לא יכול להפגין חולשה\n‫או לנהוג בחולשה")
    Message(career, tomer, u"הממ...\nזה לא העניין")
    Message(career, alon, u"‫אוקיי..")
    Message(career, tomer, u"אין לי בעיה להפגין חולשה")
    Message(career, alon, u"‫נכון")
    Message(career, tomer, u"אבל אני רוצה להתגבר על החולשה, ולא לתת לה להכתיב את ההחלטה שלי")
    Message(career, alon, u"‫מה מפחיד אותך במצב שבו לא תהיה מנהל?\n‫היום, איך שאתה?")
    Message(career, tomer, u"(סלח לי דקה, הילדים צריכים משהו)")
    Message(career, alon, u"‫אין בעיה")
    Message(career, tomer, u"חזרתי")
    Message(career, alon, u"‫כן\n‫אז מה מפחיד אותך?")
    Message(career, tomer, u"כמה דברים\nאחד, שיהיה לי מנהל שיהיה לי קשה לעבוד איתו, כי הוא ידרוש הרבה דברים או ייכנס לי לקרביים\nדבר שני, שאני אתעסק יותר מדי בפרטים טכניים ולא אהיה במרכז העניינים (שזה גם יתרון וגם חסרון)")
    Message(career, alon, u"‫אני רוצה לחזור רגע צעד אחורה\n‫ברשותך\n‫אתה יכול לתאר לי את המצב האידיאלי שבו הייתי רוצה לעבוד?\n‫בלי הגדרות תפקיד, בלי גבולות, בלי ציפיות\n‫רק מה שאתה רוצה")
    Message(career, tomer, u"אוקיי\nסביבה תומכת של אנשים שסומכים אחד על השני\nללא צורך בלוחות זמנים או התחייבות לתאריכים\nעם הערכה ליצירתיות\nעם אפשרות לעשות מנטורינג לאנשים וללמד")
    Message(career, alon, u"‫אמרת משהו על להיות במרכז העניינים. זה גם חלק?")
    Message(career, tomer, u"ברור. אני נהנה מזה שמעריכים אותי, אולי אפילו מעריצים")
    Message(career, alon, u"‫כל הכבוד על הכנות\n‫מותר לך לרצות שיעריצו אותך")
    Message(career, tomer, u"כן, גיליתי את זה כבר")
    Message(career, alon, u"‫אוקיי, מגניב, מה עוד?")
    Message(career, tomer, u"אני רוצה סביבה שמעריכה דברים שחשובים בעיני, ולא דברים שרירותיים כמו \"עוד גרסה מטופשת\"\nלעשות משהו שעוזר לאנשים, זה משמעותי.")
    Message(career, alon, u"‫אז מה שאתה אומר\n‫הוא שאתה רוצה השפעה משמעותית על סביבת העבודה שלך\n‫על האנשים שסביבך\n‫אתה רוצה תקשורת טובה עם האנשים שאתה עובד איתם\n‫ואתה רוצה חופש\n‫חופש ליצור ולעבוד עם אנשים\n‫נכון?")
    Message(career, tomer, u"נכון\nאבל אני מספר לעצמי שלמנהל אין \"חופש\"\nבגלל שהוא \"אחראי\"\nואני מבין שזה לא נכון, אבל לא ברור לי מספיק איך זה")
    Message(career, alon, u"‫איך הצלחת להפוך את אחריות להיות ההפך מחופש?")
    Message(career, tomer, u"זהו, משהו אצלי תקוע בתחום הזה\nשל בין אחריות לחופש\nרגשות האשם האלה, שחופש זה חוסר אחריות")
    Message(career, alon, u"‫מתי אחריות פוגעת בחופש?")
    Message(career, tomer, u"כשהיא מעיקה\nולא באה מתוכי אלא מבחוץ")
    Message(career, alon, u"‫וכשאתה אומר האחריות מעיקה עלי, אתה אחראי או קורבן?")
    Message(career, tomer, u"ברור שקרבן")
    Message(career, alon, u"‫כשאתה אומר האחריות באה מבחוץ, אתה אחראי או קורבן?")
    Message(career, tomer, u"קרבן. אני יודע.")
    Message(career, alon, u"‫בראש\n‫כן, זה קל בראש")
    Message(career, tomer, u"בדיוק!!\nאני לא מצליח להרגיש את זה.\nזה בדיוק העניין")
    Message(career, alon, u"‫אוקיי\n‫לאט לאט\n‫לא צריך לרוץ\n‫זה משהו שיכול לקחת לו קצת זמן לנחות מהראש ללב\n‫תנשום רגע\n‫קח נשימה עמוקה")
    Message(career, tomer, u"זה ממש כאילו אתה לידי")
    Message(career, alon, u"‫יחד עם הצמרמורות :)\n‫אתה רוצה להביא את התובנה בכוח\n‫כי אתה יודע איזו תובנה אתה רוצה להביא\n‫אבל זה לא עובד ככה\n‫לצערינו, אנשי הראש")
    Message(career, tomer, u"ממש ככה")
    Message(career, alon, u"‫אני רוצה לתת לך תרגיל אם בא לך")
    Message(career, tomer, u"טוב")
    Message(career, alon, u"‫בדרך כלל כשאנחנו מתלבטים בין שתי אפשרויות, אנחנו חושבים על זה כצומת\n‫אבל בעצם זה יותר דומה לירידה ממחלף\n‫יש דרך אחת שהיא דיפולט\n‫ואחרת שאותה אנחנו יכולים לקחת אם נבחר")
    Message(career, tomer, u"מאד מתחבר לזה")
    Message(career, alon, u"‫מה ברירת המחדל שלך כרגע בהקשר הזה?\n‫זה לא פשוט..")
    Message(career, tomer, u"זו שאלה טובה\nכי אני יכול לנמק לשני כיוונים")
    Message(career, alon, u"‫אוקיי, נשים את זה בצד לרגע\n‫הרעיון של התרגיל הוא להתחייס ברצינות לכל אחת מהאפשרויות\n‫זה כמו בעד / נגד\n‫*נגד\n‫אבל אני אוהב את המונחים מחירים / תמורות\n‫עבור כל אחת מהאפשרויות עושים טבלה עם שתי עמודות\n‫מחירים בצד אחד\n‫תמורות בצד השני\n‫בשונה מבעד ונגד, מחירים ותמורות מאפשרים להתייחס לעניינים רגשיים\n‫אין פה שום דבר אובייקטיבי\n‫לפחדים, חששות, ציפיות, אכזבות - לכל הדברים האלה יש מקום בשתי הטבלאות")
    Message(career, tomer, u"אני מבין")
    Message(career, alon, u"‫כשתמלא את הטבלאות, תסמן בכל עמודה את הדבר הכי חשוב שם\n‫את התמורה הכי גדולה ללהיות מנהל\n‫את המחיר הכי גדול\n‫וכו")
    Message(career, tomer, u"חשבתי על טבלה, אבל לא ידעתי איזו. זה עוזר.")
    Message(career, alon, u"‫זה אמור לעזור לך להתפקס על מה שאתה מרגיש\n‫יכול להיות יווצר מצב שבו שתי האפשרויות לא טובות\n‫זה רק מצביע על כך שצריך לחפש פתרונות אחרים :)")
    Message(career, tomer, u"אוקיי\nאני הולך לעבוד על זה")
    Message(career, alon, u"‫אל תשכח לנשום\n‫זה לא דחוף ברמת הדקות")
    Message(career, tomer, u"תודה")
    Message(career, alon, u"‫ואני פה אם אתה צריך אותי")

    db.session.commit()