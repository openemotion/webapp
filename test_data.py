# coding=utf-8
from model import *

def create_test_data():
    alon = User(u"אלון", u"123456")
    anat = User(u"ענת", u"123456")
    tomer = User(u"תומר", u"123456")
    db.session.add_all([alon, anat, tomer])

    relationship = Conversation(anat, u'אני מפחדת להרוס את היחסים', status=Conversation.STATUS.ACTIVE)
    post = relationship.messages.append

    post(Message(anat, u"אני בטיפול ממושך להבראת דפוסים לא בריאים\nאחרי שבמשך שנים החרבתי מערכות יחסים בזו אחר זו\nולא תכננתי להכנס למערכת היחסים הזו\nואני מאד חרדה להחריב גם אותה\nואני סובלת, ליטרלי\nכאב\nאמיתי"))
    post(Message(alon, u"מה יחריב את היחסים?"))
    post(Message(anat, u"שאני אחזור על השגיאות\nשאני לא אצליח בחיים האישיים שלי\nוזה יהפוך אותי לבן אדם שלא ראוי לחיות איתו"))
    post(Message(alon, u"מה יהפוך אותך לאדם שלא ראוי לחיות איתו?"))
    post(Message(anat, u"שאני אתקע, שאני לא אתקדם, שאני לא אוכל לתרום במידה שווה\nהקטע הכלכלי מפריע לי באופן מיוחד"))
    post(Message(alon, u"מה קורה בתחום הכלכלי?"))
    post(Message(anat, u"דווקא עשיתי קפיצה לא רעה בשנה פלוס האחרונות\nאבל\nאני לא יכולה להגיע לרמות שכר, זה נורא מפגר\nכשאני קוראת את המשפטים של עצמי\nאבל אלהים כמה שזה כואב"))
    post(Message(alon, u"מה זה אומר בשבילך שאת לא יכולה להגיע לרמות השכר של חבר שלך?"))
    post(Message(anat, u"שאני לא יכולה לתרום באותה המידה\nליחסים\nלחיים משותפים"))
    post(Message(alon, u"הוא יודע שאת מקנאה?"))
    post(Message(anat, u"ברור"))
    post(Message(alon, u"מגניב!"))
    post(Message(anat, u"אבל זה לא יוצא עליו בלייב"))
    post(Message(alon, u"למה לא?"))
    post(Message(anat, u"למדתי להוציא את זה על אנשים אחרים\nכשאני מרגישה שהמפלצת מרימה את ראשה\nאני פשוט תופסת ממנו מרחק"))
    post(Message(alon, u"למה את קוראת לזה \"להוציא\"?"))
    post(Message(anat, u"להגיד מה שאני באמת חושבת ומרגישה\nהוא אף פעם לא רואה אותי מתפרקת, רק אנשים אחרים\nכי ההתפרקויות החריבו יחסים\nבעבר\nאחד הדפוסים"))
    post(Message(alon, u"אז את מתרחקת"))
    post(Message(anat, u"נכון"))
    post(Message(alon, u"בנסיון לשמור על היחסים\nנכון?"))
    post(Message(anat, u"אמת"))
    post(Message(alon, u"תקראי את זה רגע שוב"))
    post(Message(anat, u"קראתי"))
    post(Message(alon, u"להתרחק בשביל לשמור על היחסים"))
    post(Message(anat, u"נכון\nכי יש לי הרגשה שאם אני אוציא את הדברים החוצה כמו שהם היחסים לא יחזיקו מעמד\nכמו שהיחסים הקודמים לא החזיקו מעמד"))
    post(Message(alon, u"סיפרת בשיחה קודמת שהוא התאהב בך כשסיפרת לו את הדברים הכי רעים עלייך"))
    post(Message(anat, u"נכון\nלא מדויק -\nמה שקרה הוא\nשסיפרתי דברים רעים כי לא רציתי לעמוד בפני הדילמה הזאת\nוזה דווקא מה שקרב בינינו"))
    post(Message(alon, u"אני רוצה להגיד לך שאת תותחית על חלל\nרק על הקטע הזה שנכנסת בעובי הקורה\nבשתי דקות של שיחה"))
    post(Message(anat, u"תודה"))
    post(Message(alon, u"בבקשה\nאוקיי\nאז כשהכרתם, דברים שסיפרת לו שחשבת שירחיקו אותו ממך, גרמו לו להתקרב"))
    post(Message(anat, u"נכון"))
    post(Message(alon, u"ומה קורה עכשיו?\nמה שונה עכשיו?"))
    post(Message(anat, u"זה נעצר\nאני לא יכולה להוציא את מה שנראה בעיני מפלצת"))
    post(Message(alon, u"אז מה מפלצתי בך?"))
    post(Message(anat, u"אני קנאית\nיש לי מצבי רוח רעים\nאני לא רוצה להרגיש שאני תופסת את כל המקום\nולא נותנת מקום\nיש לי חרדות המוות מלא להצליח\nיש לי היסטוריה לא מפוארת ודפוסי התנהגות שממש פחיד אותי שהם יחזרו\nנראה לי שסיכמתי"))
    post(Message(alon, u"מה הכי נורא מכל אלה?"))
    post(Message(anat, u"שאלה טובה\nקשה לי להגיד\nאולי הקנאה,\nהיא לא הכי נוראה\nאבל היא הכי מכאיבה\nוכשהיא מכאיבה\nאני יודעת שהיא לא הגיונית\nאבל היא ממש מכאיבה לי"))
    post(Message(alon, u"מה את הכי מפחדת שהוא ידע?"))
    post(Message(anat, u"איך הקנאה שלי נראית"))
    post(Message(alon, u"ואיך היא נראית?"))
    post(Message(anat, u"רע"))
    post(Message(alon, u"ספרי לי"))
    post(Message(anat, u"אני שונאת אותן"))
    post(Message(alon, u"אותן?"))
    post(Message(anat, u"כן"))
    post(Message(alon, u"נשים אחרות?"))
    post(Message(anat, u"כן"))
    post(Message(alon, u"יש מישהי ספציפית?"))
    post(Message(anat, u"לא\nיש הרבה"))
    post(Message(alon, u"הרבה ספציפיות, או כל בחורה שמסתכלת עליו?"))
    post(Message(anat, u"הרבה ספציפיות"))
    post(Message(alon, u"הקנאה זה מה שהרס את היחסים הקודמים שלך?"))
    post(Message(anat, u"ממש לא\nאבל הכעס\nוהדרך שביטאתי אותו\nכן"))
    post(Message(alon, u"ועל מה כעסת?"))
    post(Message(anat, u"וואו\nעל מיליון דברים"))
    post(Message(alon, u"מה הדבר הראשון שקופץ לך לראש?"))
    post(Message(anat, u"*****\nשתמות\nזה פשוט גם גילוי של קנאה"))
    post(Message(alon, u"על מה כעסת עליה?"))
    post(Message(anat, u"שהיא באה ונכנסה לי לחיים\nודרסה אותי בניסיון להשיג את מה שהיא רצתה\nשהיא נכנסה לטריטוריה שלי, לבית שלי\nודרכה עלי"))
    post(Message(alon, u"אני רוצה לשמוע יותר על *****\nמה בדיוק היא עשתה\nומה בדיוק הרגשת"))
    post(Message(anat, u"טוב\nזה נחלק לשני חלקים\nהחלק הראשון הוא כשעוד הייתי עם *****\nנכנסתי הביתה ותפסתי אותם על חם כמו בסרטים\nהפרעתי להם באמצע\nוהחלק השני היה\nשהוא הלך אליה וגר אצלה\nשזה כבר לא כעס עליה אלא עליו\nזה כבר לא מזיז לי היום"))
    post(Message(alon, u"ובפעם הראשונה לא כעסת עליו?"))
    post(Message(anat, u"לא"))
    post(Message(alon, u"רק עליה?"))
    post(Message(anat, u"כן\nרק עליה"))
    post(Message(alon, u"לא ראית בו אחראי?"))
    post(Message(anat, u"לא\nממש ככה"))
    post(Message(alon, u"לא ראית אותו ממטר"))
    post(Message(anat, u"דווקא ראיתי\nאחרי זה, בפעם השניה\nראיתי אותו גם"))
    post(Message(alon, u"ומה קורה לך במערכת היחסים הנוכחית?\nתפסת את ***** עם מישהי?"))
    post(Message(anat, u"ממש לא\nאני מרגישה בעיקר כאב\nבכל מיני סיטואציות\nכאב פיזי ממש"))
    post(Message(alon, u"איפה?"))
    post(Message(anat, u"איפה בגוף?"))
    post(Message(alon, u"כן"))
    post(Message(anat, u"בבטן, בחזה\nכשאני רואה כל מיני דברים או עדה לכל מיני דברים"))
    post(Message(alon, u"מה את רואה שמקפיץ לך את הכאב?"))
    post(Message(anat, u"אז הדוגמה העיקרית היא *****\nואיך שהיא מתנהגת\nמהיום שהכרנו בערך\nמה שמקפיץ לי...\nשהיא מזמינה אותו לארוחות ערב לבד\nשהיא אומרת לי שהיא פספסה הזדמנות לאהבה אמיתית שהיתה \"כמעט\"\nשהיא מסרבת פאקינג ללכת\nוחייבת להשאר בתמונה כל הזמן\nאבל זה לא רק היא\nזה גם כל מיני אקסיות שעושות \"לייקים\" לתמונות\nכוס אמא של העידן המודרני"))
    post(Message(alon, u"\nאז את רוצה את ***** רק לעצמך?"))
    post(Message(anat, u"כן ולא\nבן אדם \"טוב\" תמיד ימשוך תשומת לב חיובית\nזה בא עם החבילה\nזה החלק ההגיוני\nאני פשוט לא יודעת להתמודד עם זה"))
    post(Message(alon, u"את רוצה שזה לא יגרום לך כאב?"))
    post(Message(anat, u"בדיוק"))
    post(Message(alon, u"למה?"))
    post(Message(anat, u"כי אני סובלת\nואני רוצה להפסיק לסבול"))
    post(Message(alon, u"האם את סובלת בגלל שכואב, או שאת סובלת בגלל שאת לא רוצה שיכאב?\nאת מבינה את הכוונה שלי?"))
    post(Message(anat, u"לא"))
    post(Message(alon, u"אוקיי\nנניח שיש חייל\nוהוא נפצע\nוהוא שוכב בבית החולים\nוכואב לו נורא\nבפצעים\nאבל בנוסף לכל זה\nהוא חושב שהוא בכלל לא היה אמור להפצע\nאם הוא רק היה מתקופף"))
    post(Message(anat, u"כן, מבינה"))
    post(Message(alon, u"אז השאלה היא האם הבעיה היא הכאב, או המחשבה שמתלווה אליו?"))
    post(Message(anat, u"לא. זה הכאב.\nיש עוד משהו\nעכשיו כשאני חושבת על זה\nתמיד חשבתי על שני הדברים אבל אף פעם לא קישרתי\nמאד מפריע לי שבעולם \"הוירטואלי\"\nאף אחד לא יודע מי אני\nואני מרגישה שזה לא לגיטימי לבוא ולדרוש שזה יהיה אחרת\nואני מרגישה שזה לא לגיטימי שאני אגיד את זה אפילו\nאבל\nמי שמכיר את ***** בעולם הוירטואלי לא מכיר אותי\nוזה הולך ביחד"))
    post(Message(alon, u"אני לא בטוח שהבנתי מה הבנת\nמה הבנת?"))
    post(Message(anat, u"שזה לא רק הן\nזה גם דברים בדרך שלו שמפריעים לי\nואני לא מסוגלת אפילו להגיד את זה\nכי רק מלקרוא את השורות שאני כותבת עכשיו\nזה נראה לי לא לגיטימי"))
    post(Message(alon, u"זה נורא כיף לראות אותך עובדת\nומתעמקת\nומחפשת"))
    post(Message(anat, u"כן. ועכשיו כואבת לי הבטן. והחזה. והלב.\nמהדברים הדבילים האלה"))
    post(Message(alon, u"או\nרגע\nעצרי\nלמה אלה דברים דביליים?\nאלה הרגשות שלך"))
    post(Message(anat, u"נכון"))
    post(Message(alon, u"אוקיי\nאז הרגשות שלך דביליות?\nבואי נסתכל על משהו רגע\nמה הדבר שהכי מפחיד אותך להגיד ל*****?"))
    post(Message(anat, u"קשה לי להצביע על משפט אחד\nבערך כל מה שאמרתי לך עכשיו"))
    post(Message(alon, u"ובכל זאת\nמה הדבר שהחשיפה שלו מעוררת הכי הרבה כאב?"))
    post(Message(anat, u"אולי זה הדבר שהכי מפחיד אותי להגיד\nשההתנהגות החשאית הזאת של *****\nמזמינה את זה\nמזמינה אותן\nודבר שני\nאני רוצה שיתגאו בי"))
    post(Message(alon, u"למה חשוב לך ש***** יתגאה בך?"))
    post(Message(anat, u"אררר\nשאלה קשה\nאני מניחה שזה חוזר למה שדיברנו עליו בהתחלה\nלהרגיש בן אדם ראוי\nופה יש גם חלק שהוא שלי"))
    post(Message(alon, u"אם ***** יתגאה בך, את תרגישי ראויה?\nאו שאם תרגישי ראויה, אז ***** יתגאה בך?"))
    post(Message(anat, u"שניהם\nאבל ברור שאני צריכה ללמוד להרגיש ראויה ללא קשר"))
    post(Message(alon, u"איך יראו החיים שלך כשתרגישי לגמרי ראויה?\nמה יקרה?"))
    post(Message(anat, u"קלילים ונעימים"))
    post(Message(alon, u""))
    post(Message(anat, u"ואני לא אתעצבן מאיזה סתומה שעושה לייק\nאני לא אפחד ואני לא אתרגש מהשטויות האלה"))
    post(Message(alon, u"אהו!\nנכון\nהפאקצות ימשיכו להציק\n***** ימשיך להסתיר\nואת?"))
    post(Message(anat, u"זה לא יזיז לי\nכי אני ארגיש כזה בן אדם נפלא\nשאני לא אצטרך את החיזוקים האלה מבחוץ"))
    post(Message(alon, u"מה שלום הכאב?"))
    post(Message(anat, u"וואללה\nיש עוד עבודה\nאני יודעת שזה הכיוון"))
    post(Message(alon, u"מה את יכולה לעשות בכדי להרגיש יותר ראויה?\nמשהו שלא תלוי באף אחד אחר.."))
    post(Message(anat, u"לא יודעת, זה מעסיק אותי המון\nלא משהו חיצוני כנראה כי דברים דווקא מסתדרים לי מצויין חיצונית\nוזה לא עוזר"))
    post(Message(alon, u"מה קרה בשיחה הזאת עכשיו?\nמה שיפר את ההרגשה שלך?"))
    post(Message(anat, u"שדימיינתי את המצב הרצוי"))
    post(Message(alon, u"אז בואי תקחי את זה צעד אחד קדימה\nתתארי בכתב איך יראו החיים שלך\nכשתרגישי ראויה"))
    post(Message(anat, u"אוקיי"))
    post(Message(alon, u"שיעורי בית"))
    post(Message(anat, u"אחלה\nחפרנו"))

    career = Conversation(tomer, u'אני מתלבט אם לקחת אחריות ולהיות מנהל', status=Conversation.STATUS.ACTIVE)
    post = career.messages.append

    post(Message(tomer, u"אני בהתלבטות מאד קשה, ורוצה קצת שיקופים\nבעקבות הסדנה, בהמלצה של המאמנת, התחלתי קצת לכתוב דברים (ואני לא מתכוון לקוד)\nופתאום שמתי לב שיש לי עניין לא פתור לגבי החלפת התפקיד שלי בעבודה"))
    post(Message(alon, u"‫ואללה\n‫מעניין"))
    post(Message(tomer, u"ואני מאד מתלבט אם הרצון להחליף תפקיד נובע מרצון אמיתי להתנתק מתפקיד רשמי וניהולי ולהשתחרר מתכנון והערכות זמנים ואחריות, או...\nאו שזה פשוט תירוץ לחשוב שאם רק אחליף תפקיד, הכל יהיה יותר טוב (ומושלם)."))
    post(Message(alon, u"‫ומה יצא לך בכתיבה?"))
    post(Message(tomer, u"זהו, השאלה עלתה, ועדיין אין תשובה. אבל יש לי הרגשה מאד חזקה שזה לא באמת יעשה שינוי משמעותי."))
    post(Message(alon, u"‫איזה שינוי אתה רוצה שיקרה?"))
    post(Message(tomer, u"ובאותה מידה אני יכול להישאר בתפקיד, ולעשות אותו איך שאני חושב שצריך לעשות אותו.\nההיפך: ראיתי המון הערכה על הכנות."))
    post(Message(alon, u"‫אני רוצה לחזור על שאלה שלי - מה אתה רוצה שיקרה?\n‫הרי עשית את הצעד הזה בשביל להשיג משהו, מה זה?"))
    post(Message(tomer, u"(חושב)"))
    post(Message(alon, u"‫רק אם תדע את התשובה, תוכל לדעת האם הצעד מקרב אותך לשם או לא.."))
    post(Message(tomer, u"אני רוצה להרגיש טוב עם מה שאני עושה. אני לא רוצה לעשות דברים בשביל לרצות אף אחד."))
    post(Message(alon, u":)\n‫ואיך זה קשור למציאות בחוץ?"))
    post(Message(tomer, u"לא רוצה לרצות את הבוס שלי, ולא את הקולגות שלי.\nואני מספר לעצמי שהם מצפים ממני לעשות דברים באופן מסויים, לא כמו שאני חושב שצריך לעשות.\nובנושא הטכני, יש לי ביטחון עצמי גבוה שאני יודע מה נכון"))
    post(Message(alon, u"‫יצא לך לחשוב על איך היית רוצה לעשות את התפקיד בעולם מושלם?"))
    post(Message(tomer, u"למרות שהיתה לי תקופה קשה גם בזה, כפי שסיפרתי לך"))
    post(Message(alon, u"‫בלי ציפיות מאחרים ובלי רגשות אשם שלך?"))
    post(Message(tomer, u"כן! בדיוק."))
    post(Message(alon, u"‫איך זה יראה?"))
    post(Message(tomer, u"ובחודשים האחרונים אני מרגיש שאני עושה את התפקיד בצורה הכי טובה עד כה.\nלא עושה ישיבות עם האנשים פעם בשבוע \"כי צריך\"\nלא עושה תכניות עבודה \"כי צריך\"\nפשוט זורם"))
    post(Message(alon, u"‫ומה הבעיה עם זה?"))
    post(Message(tomer, u"זהו, שגיליתי שאין שום בעיה עם זה.\nלהיפך\nפשוט האמנתי שאני לא מנהל טוב.\nאני זוכר ש*** ב****** התפלא מאד כשאמרתי לי שאני לא חושב שאני מתאים להיות ראש צוות\nהוא אמר שאני אחד הר\"צ הכי טובים שלו\nאמרתי לעצמי שבוא סתם שקרן ורוצה שקט תעשייתי\nואולי הוא לא שיקר"))
    post(Message(alon, u"‫מתי הגעת למסקנה שאתה ראש צוות לא טוב?\n‫זה היה לפני ****** אני מניח.."))
    post(Message(tomer, u"נראה לי שזה גם שריד מ******.\nשם הייתי פשוט \"לא טוב\"."))
    post(Message(alon, u"‫ואו.. הרבה זמן עבר מאז"))
    post(Message(tomer, u"הייתי troublemaker"))
    post(Message(alon, u"‫וזה בעיניך היום דבר לא טוב?"))
    post(Message(tomer, u"ולא שיתפתי פעולה עם אנשים, כי ידעתי איך לעשות הכל \"נכון\" והם לא.\nהיום אני חושב שלהיות troublemaker זה פשוט לא אפקטיבי.\nזה שוחק אותי ואת הסביבה\nולא משיג תוצאות חוץ מתסכול משני הצדדים"))
    post(Message(alon, u"‫נכון\n‫ואתה גם לא רוצה להיות כנוע\n‫ולעשות מה שאומרים לך ומה שמצפים ממך"))
    post(Message(tomer, u"נכון."))
    post(Message(alon, u"‫והאמת איננה באמצע"))
    post(Message(tomer, u"אבל עכשיו אני יכול לראות את הדברים דרך העיניים של אנשים אחרים\nולהבין שאני יכול לעזור להם ולהרגיש טוב\nבלי לרצות אותם"))
    post(Message(alon, u"‫ואו!"))
    post(Message(tomer, u"זה קרה לי השבוע כמה פעמים בעבודה."))
    post(Message(alon, u"‫זה מטורף מה שאתה אומר\n‫אז רגע"))
    post(Message(tomer, u"וההרגשה היתה נפלאה, לעזור כי אני רוצה."))
    post(Message(alon, u"‫מה הבעיה?\n‫אמרת שיש בעיה"))
    post(Message(tomer, u"זהו שאין בעיה"))
    post(Message(alon, u"‫אני לא רואה בעיה :)"))
    post(Message(tomer, u"יש בעיה קטנה"))
    post(Message(alon, u"אוקיי.."))
    post(Message(tomer, u"שאני חושש שאם אשאר בתפקיד, זה מתוך פחד של מה תהיה האלטרנטיבה\nכמו שהיה כשקיבלתי את התפקיד\nולא מתוך רצון אמיתי\nואת זה אני רוצה לחקור"))
    post(Message(alon, u"‫ואתה מנסה להבין מהו רצון אמיתי ומהו פחד?"))
    post(Message(tomer, u"בדיוק"))
    post(Message(alon, u"‫אוקיי\n‫למה לפעול מתוך פחד זה לא נכון?\n‫זה בהכרח לא נכון?"))
    post(Message(tomer, u"*צוחק*"))
    post(Message(alon, u":)"))
    post(Message(tomer, u"זה נראה לי כמו חולשה"))
    post(Message(alon, u"‫אה..\n‫ואתה לא יכול להפגין חולשה\n‫או לנהוג בחולשה"))
    post(Message(tomer, u"הממ...\nזה לא העניין"))
    post(Message(alon, u"‫אוקיי.."))
    post(Message(tomer, u"אין לי בעיה להפגין חולשה"))
    post(Message(alon, u"‫נכון"))
    post(Message(tomer, u"אבל אני רוצה להתגבר על החולשה, ולא לתת לה להכתיב את ההחלטה שלי"))
    post(Message(alon, u"‫מה מפחיד אותך במצב שבו לא תהיה מנהל?\n‫היום, איך שאתה?"))
    post(Message(tomer, u"(סלח לי דקה, הילדים צריכים משהו)"))
    post(Message(alon, u"‫אין בעיה"))
    post(Message(tomer, u"חזרתי"))
    post(Message(alon, u"‫כן\n‫אז מה מפחיד אותך?"))
    post(Message(tomer, u"כמה דברים\nאחד, שיהיה לי מנהל שיהיה לי קשה לעבוד איתו, כי הוא ידרוש הרבה דברים או ייכנס לי לקרביים\nדבר שני, שאני אתעסק יותר מדי בפרטים טכניים ולא אהיה במרכז העניינים (שזה גם יתרון וגם חסרון)"))
    post(Message(alon, u"‫אני רוצה לחזור רגע צעד אחורה\n‫ברשותך\n‫אתה יכול לתאר לי את המצב האידיאלי שבו הייתי רוצה לעבוד?\n‫בלי הגדרות תפקיד, בלי גבולות, בלי ציפיות\n‫רק מה שאתה רוצה"))
    post(Message(tomer, u"אוקיי\nסביבה תומכת של אנשים שסומכים אחד על השני\nללא צורך בלוחות זמנים או התחייבות לתאריכים\nעם הערכה ליצירתיות\nעם אפשרות לעשות מנטורינג לאנשים וללמד"))
    post(Message(alon, u"‫אמרת משהו על להיות במרכז העניינים. זה גם חלק?"))
    post(Message(tomer, u"ברור. אני נהנה מזה שמעריכים אותי, אולי אפילו מעריצים"))
    post(Message(alon, u"‫כל הכבוד על הכנות\n‫מותר לך לרצות שיעריצו אותך"))
    post(Message(tomer, u"כן, גיליתי את זה כבר"))
    post(Message(alon, u"‫אוקיי, מגניב, מה עוד?"))
    post(Message(tomer, u"אני רוצה סביבה שמעריכה דברים שחשובים בעיני, ולא דברים שרירותיים כמו \"עוד גרסה מטופשת\"\nלעשות משהו שעוזר לאנשים, זה משמעותי."))
    post(Message(alon, u"‫אז מה שאתה אומר\n‫הוא שאתה רוצה השפעה משמעותית על סביבת העבודה שלך\n‫על האנשים שסביבך\n‫אתה רוצה תקשורת טובה עם האנשים שאתה עובד איתם\n‫ואתה רוצה חופש\n‫חופש ליצור ולעבוד עם אנשים\n‫נכון?"))
    post(Message(tomer, u"נכון\nאבל אני מספר לעצמי שלמנהל אין \"חופש\"\nבגלל שהוא \"אחראי\"\nואני מבין שזה לא נכון, אבל לא ברור לי מספיק איך זה"))
    post(Message(alon, u"‫איך הצלחת להפוך את אחריות להיות ההפך מחופש?"))
    post(Message(tomer, u"זהו, משהו אצלי תקוע בתחום הזה\nשל בין אחריות לחופש\nרגשות האשם האלה, שחופש זה חוסר אחריות"))
    post(Message(alon, u"‫מתי אחריות פוגעת בחופש?"))
    post(Message(tomer, u"כשהיא מעיקה\nולא באה מתוכי אלא מבחוץ"))
    post(Message(alon, u"‫וכשאתה אומר האחריות מעיקה עלי, אתה אחראי או קורבן?"))
    post(Message(tomer, u"ברור שקרבן"))
    post(Message(alon, u"‫כשאתה אומר האחריות באה מבחוץ, אתה אחראי או קורבן?"))
    post(Message(tomer, u"קרבן. אני יודע."))
    post(Message(alon, u"‫בראש\n‫כן, זה קל בראש"))
    post(Message(tomer, u"בדיוק!!\nאני לא מצליח להרגיש את זה.\nזה בדיוק העניין"))
    post(Message(alon, u"‫אוקיי\n‫לאט לאט\n‫לא צריך לרוץ\n‫זה משהו שיכול לקחת לו קצת זמן לנחות מהראש ללב\n‫תנשום רגע\n‫קח נשימה עמוקה"))
    post(Message(tomer, u"זה ממש כאילו אתה לידי"))
    post(Message(alon, u"‫יחד עם הצמרמורות :)\n‫אתה רוצה להביא את התובנה בכוח\n‫כי אתה יודע איזו תובנה אתה רוצה להביא\n‫אבל זה לא עובד ככה\n‫לצערינו, אנשי הראש"))
    post(Message(tomer, u"ממש ככה"))
    post(Message(alon, u"‫אני רוצה לתת לך תרגיל אם בא לך"))
    post(Message(tomer, u"טוב"))
    post(Message(alon, u"‫בדרך כלל כשאנחנו מתלבטים בין שתי אפשרויות, אנחנו חושבים על זה כצומת\n‫אבל בעצם זה יותר דומה לירידה ממחלף\n‫יש דרך אחת שהיא דיפולט\n‫ואחרת שאותה אנחנו יכולים לקחת אם נבחר"))
    post(Message(tomer, u"מאד מתחבר לזה"))
    post(Message(alon, u"‫מה ברירת המחדל שלך כרגע בהקשר הזה?\n‫זה לא פשוט.."))
    post(Message(tomer, u"זו שאלה טובה\nכי אני יכול לנמק לשני כיוונים"))
    post(Message(alon, u"‫אוקיי, נשים את זה בצד לרגע\n‫הרעיון של התרגיל הוא להתחייס ברצינות לכל אחת מהאפשרויות\n‫זה כמו בעד / נגד\n‫*נגד\n‫אבל אני אוהב את המונחים מחירים / תמורות\n‫עבור כל אחת מהאפשרויות עושים טבלה עם שתי עמודות\n‫מחירים בצד אחד\n‫תמורות בצד השני\n‫בשונה מבעד ונגד, מחירים ותמורות מאפשרים להתייחס לעניינים רגשיים\n‫אין פה שום דבר אובייקטיבי\n‫לפחדים, חששות, ציפיות, אכזבות - לכל הדברים האלה יש מקום בשתי הטבלאות"))
    post(Message(tomer, u"אני מבין"))
    post(Message(alon, u"‫כשתמלא את הטבלאות, תסמן בכל עמודה את הדבר הכי חשוב שם\n‫את התמורה הכי גדולה ללהיות מנהל\n‫את המחיר הכי גדול\n‫וכו"))
    post(Message(tomer, u"חשבתי על טבלה, אבל לא ידעתי איזו. זה עוזר."))
    post(Message(alon, u"‫זה אמור לעזור לך להתפקס על מה שאתה מרגיש\n‫יכול להיות יווצר מצב שבו שתי האפשרויות לא טובות\n‫זה רק מצביע על כך שצריך לחפש פתרונות אחרים :)"))
    post(Message(tomer, u"אוקיי\nאני הולך לעבוד על זה"))
    post(Message(alon, u"‫אל תשכח לנשום\n‫זה לא דחוף ברמת הדקות"))
    post(Message(tomer, u"תודה"))
    post(Message(alon, u"‫ואני פה אם אתה צריך אותי"))

    db.session.commit()