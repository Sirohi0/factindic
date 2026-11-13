"""Small Hindi -> English lexicon of nouns and adjectives that Hindi news text often mixes in.

Used by codemix.py to turn Hindi text into Devanagari + Latin code-mixed text by *inserting*
English words into Hindi sentence frames (insertion-style mixing). Only whole Devanagari words
that appear here are replaced; names, numbers, dates and verbs are never touched, so the facts
in a document cannot change. Extend this file to raise the amount of mixing.
"""
import unicodedata

_RAW = """
सरकार=government मंत्री=minister मंत्रालय=ministry प्रधानमंत्री=prime-minister मुख्यमंत्री=chief-minister
चुनाव=election पार्टी=party नेता=leader नेताओं=leaders विपक्ष=opposition संसद=parliament विधानसभा=assembly
राज्य=state राज्यों=states योजना=scheme योजनाओं=schemes नीति=policy कानून=law अदालत=court न्यायालय=court
फैसला=decision फैसले=decisions आदेश=order मामला=case मामले=cases जांच=investigation अधिकारी=officer
अधिकारियों=officers सचिव=secretary राष्ट्रपति=president राज्यपाल=governor सांसद=MP विधायक=MLA प्रशासन=administration
आयोग=commission समिति=committee बैठक=meeting सम्मेलन=conference घोषणा=announcement रिपोर्ट=report बयान=statement
आरोप=allegation सुरक्षा=security सेना=army जवान=soldier आतंकवादी=terrorist हमला=attack हिंसा=violence
विरोध=protest प्रदर्शन=demonstration आंदोलन=movement शिकायत=complaint मुकदमा=lawsuit
अर्थव्यवस्था=economy बाजार=market कंपनी=company कंपनियों=companies कारोबार=business व्यापार=trade निवेश=investment
टैक्स=tax बजट=budget कीमत=price कीमतों=prices दाम=price महंगाई=inflation रोजगार=employment नौकरी=job
नौकरियां=jobs वेतन=salary उद्योग=industry उत्पादन=production आयात=import निर्यात=export ऋण=loan कर्ज=loan
ग्राहक=customer उपभोक्ता=consumer सेवा=service सेवाएं=services
स्वास्थ्य=health अस्पताल=hospital डॉक्टर=doctor डॉक्टरों=doctors मरीज=patient मरीजों=patients बीमारी=disease
इलाज=treatment दवा=medicine दवाइयां=medicines टीका=vaccine टीकाकरण=vaccination संक्रमण=infection महामारी=pandemic
शिक्षा=education स्कूल=school विद्यालय=school स्कूलों=schools विश्वविद्यालय=university महाविद्यालय=college
छात्र=student छात्रों=students छात्रा=student शिक्षक=teacher शिक्षकों=teachers परीक्षा=exam परिणाम=result
पाठ्यक्रम=syllabus
पर्यावरण=environment प्रदूषण=pollution जलवायु=climate तापमान=temperature स्तर=level बारिश=rain बाढ़=flood
सूखा=drought भूकंप=earthquake ऊर्जा=energy बिजली=electricity पानी=water तकनीक=technology प्रौद्योगिकी=technology
विज्ञान=science वैज्ञानिक=scientist वैज्ञानिकों=scientists अनुसंधान=research शोध=research मोबाइल=mobile
कंप्यूटर=computer सॉफ्टवेयर=software ऐप=app डेटा=data नेटवर्क=network
खिलाड़ी=player खिलाड़ियों=players टीम=team मैच=match कप्तान=captain जीत=win हार=defeat टूर्नामेंट=tournament
प्रतियोगिता=competition फिल्म=film फिल्मों=films अभिनेता=actor अभिनेत्री=actress गाना=song कलाकार=artist
निर्देशक=director
समस्या=problem समस्याओं=problems समाधान=solution जानकारी=information खबर=news समाचार=news कार्यक्रम=programme
अभियान=campaign परियोजना=project सड़क=road यातायात=traffic वाहन=vehicle गाड़ी=car रेल=train उड़ान=flight
यात्री=passenger यात्रियों=passengers यात्रा=trip पर्यटक=tourist पर्यटन=tourism होटल=hotel धर्म=religion
मंदिर=temple इतिहास=history संस्कृति=culture समाज=society परिवार=family महिला=woman महिलाओं=women
बच्चे=children बच्चों=children युवा=youth लोग=people लोगों=people नागरिक=citizen नागरिकों=citizens जनता=public
किसान=farmer किसानों=farmers फसल=crop कृषि=agriculture खेती=farming
साल=year वर्ष=year महीना=month महीने=months सप्ताह=week घंटे=hours मिनट=minute समय=time दिन=day
प्रतिशत=percent आंकड़े=figures आंकड़ों=figures संख्या=number औसत=average दर=rate क्षेत्र=area इलाका=area
इलाके=areas शहर=city शहरों=cities गांव=village गांवों=villages जिला=district देश=country देशों=countries
दुनिया=world विश्व=world अंतरराष्ट्रीय=international राष्ट्रीय=national स्थानीय=local सार्वजनिक=public निजी=private
आधिकारिक=official महत्वपूर्ण=important गंभीर=serious मुख्य=main चिंता=concern खतरा=danger जोखिम=risk
सुधार=improvement बदलाव=change परिवर्तन=change विकास=development प्रगति=progress मुद्दा=issue मुद्दे=issues
विषय=topic अवसर=opportunity चुनौती=challenge चुनौतियां=challenges लक्ष्य=target नतीजा=outcome असर=impact
प्रभाव=impact कारण=reason स्थिति=situation हालात=situation मदद=help सहायता=support समर्थन=support
निर्णय=decision प्रस्ताव=proposal रिकॉर्ड=record सूची=list आवेदन=application अपील=appeal पुरस्कार=award
सम्मान=honour अनुभव=experience जीवन=life शक्ति=power मांग=demand आपूर्ति=supply सुविधा=facility
सुविधाएं=facilities व्यवस्था=system प्रणाली=system साधन=resources संसाधन=resources
"""


def _parse() -> dict:
    lex = {}
    for pair in _RAW.split():
        hi, en = pair.split("=")
        lex[unicodedata.normalize("NFC", hi)] = en.replace("-", " ")
    return lex


LEXICON = _parse()
