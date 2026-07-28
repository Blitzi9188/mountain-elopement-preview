#!/usr/bin/env python3
# Multilingual generator (EN root, /de/, /es/) mirroring the live URL structure.
import os, json, re, html as _html
ROOT = os.path.dirname(os.path.abspath(__file__))
DOMAIN = 'https://mountain-elopement.com'

# Cloudflare Turnstile — öffentlicher Site-Key (darf im HTML stehen).
# Default = Cloudflares ALWAYS-PASSES-Testkey. Vor dem echten Livegang gegen den
# richtigen Site-Key aus dem Cloudflare-Dashboard tauschen (Secret liegt als Env-Var).
TURNSTILE_SITEKEY = '1x00000000000000000000AA'
CONTACT_ENDPOINT  = '/api/contact'

GTM_ID='GTM-MT6KGS4F'
GTM_HEAD="<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src='https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);})(window,document,'script','dataLayer','"+GTM_ID+"');</script>"
GTM_BODY='<noscript><iframe src="https://www.googletagmanager.com/ns.html?id='+GTM_ID+'" height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>'

LANGS = ['en','de','es','it']         # en = default at root
LNAME = {'en':'EN','de':'DE','es':'ES','it':'IT'}
HREFLANG = {'en':'en','de':'de','es':'es','it':'it'}

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
 '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
 '<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600;700;800&'
 'family=Newsreader:ital,opsz,wght@0,6..72,300;0,6..72,400;0,6..72,500;1,6..72,300;1,6..72,400&display=swap" rel="stylesheet">')

P_PLAN = ('Dolomites Wedding Planner', 'https://www.dolomitesweddingplanner.com/de')
P_FILM = ('No Matter The Weather', 'https://nomattertheweather.it')
P_MUA  = ('Blitzkneisser', 'https://blitzkneisser.com')
NAME_PLAN, NAME_PHOTO, NAME_FILM = 'Jlenia', 'Andreas', 'Stefanie'
TEAM_HERO = ['img/team/team-bw.webp', 'img/team/team-ski.webp', 'img/team/team-lake.webp']

def lbase(lang): return '' if lang=='en' else lang+'/'
def u(P,lang,rel): return P + lbase(lang) + rel + 'index.html'   # internal link
def depth_of(lang,rel):
    seg=[s for s in (lbase(lang)+rel).split('/') if s]
    return len(seg)
def prefix(lang,rel): return '../'*depth_of(lang,rel)

# ---------------- Translations ----------------
T = {
 'nav': {'welcome':{'en':'Welcome','de':'Willkommen','es':'Inicio'},
         'howto':{'en':'Guide','de':'Guide','es':'Guía'},
         'stories':{'en':'Stories','de':'Stories','es':'Historias'},
         'packages':{'en':'Price List','de':'Preise','es':'Precios'},
         'team':{'en':'Team','de':'Team','es':'Equipo'},
         'contact':{'en':'Contact','de':'Kontakt','es':'Contacto'}},
 'booking':{'en':'Now booking 2027 &middot; 2028 dates','de':'Buchbar 2027 &middot; Termine 2028','es':'Reservas 2027 &middot; fechas 2028'},
 'booking_link':{'en':'on request','de':'auf Anfrage','es':'a consulta'},
 # footer
 'f_tag':{'en':'Editorial elopement photography &amp; planning in the Dolomites and the Alps.',
          'de':'Editorial-Elopement-Fotografie &amp; Planung in den Dolomiten/Alpen.',
          'es':'Fotografía y planificación editorial de elopements en los Dolomitas y los Alpes.'},
 'f_explore':{'en':'Explore','de':'Entdecken','es':'Explorar'},
 'f_team':{'en':'Our Team','de':'Unser Team','es':'Nuestro equipo'},
 'f_role_photo':{'en':'Photo','de':'Foto','es':'Foto'},
 'f_role_plan':{'en':'Planning','de':'Planung','es':'Planificación'},
 'f_role_film':{'en':'Film','de':'Film','es':'Film'},
 'f_role_mua':{'en':'Make-up','de':'Make-up','es':'Maquillaje'},
 'f_imprint':{'en':'Imprint','de':'Impressum','es':'Aviso legal'},
 'f_privacy':{'en':'Privacy Policy','de':'Datenschutz','es':'Privacidad'},
 # generic buttons
 'view_all':{'en':'View all stories','de':'Alle Stories ansehen','es':'Ver todas las historias'},
 'start_planning':{'en':'Start planning','de':'Planung starten','es':'Empezar a planear'},
 'get_in_touch':{'en':'Get in touch','de':'Kontakt aufnehmen','es':'Contáctanos'},
 'visit':{'en':'Visit','de':'Ansehen','es':'Visitar'},
 'request':{'en':'Request','de':'Anfragen','es':'Solicitar'},
 # team section (shared)
 'tm_kick':{'en':'The Dream Team','de':'Das Dream-Team','es':'El Dream Team'},
 'tm_over':{'en':'Behind your day','de':'Hinter eurem Tag','es':'Detrás de vuestro día'},
 'tm_h':{'en':'The team behind<br>your elopement','de':'Das Team hinter<br>eurem Elopement','es':'El equipo detrás<br>de vuestro elopement'},
 'tm_r1':{'en':'Planning &amp; Coordination','de':'Planung &amp; Koordination','es':'Planificación y coordinación'},
 'tm_r2':{'en':'Elopement Film','de':'Elopement-Film','es':'Film de elopement'},
 'tm_r3':{'en':'Hair &amp; Make-up','de':'Hair &amp; Make-up','es':'Peluquería y maquillaje'},
 'tm_d1':{'en':'Our planning partner in the Dolomites &mdash; logistics, permits, accommodation and every detail handled on the ground, so you can simply be present. With years of experience and having grown up in the heart of the Dolomites, she knows every stone &mdash; which makes for a wonderfully relaxed atmosphere.',
          'de':'Unsere Planungspartnerin in den Dolomiten &mdash; Logistik, Genehmigungen, Unterkunft und jedes Detail vor Ort geregelt, damit ihr einfach nur da sein könnt. Mit jahrelanger Erfahrung und inmitten der Dolomiten aufgewachsen, kennt sie jeden Stein &mdash; das sorgt für eine herrlich entspannte Atmosphäre.',
          'es':'Nuestra planner en los Dolomitas &mdash; logística, permisos, alojamiento y cada detalle resuelto sobre el terreno, para que solo tengáis que estar presentes. Con años de experiencia y criada en el corazón de los Dolomitas, conoce cada piedra &mdash; lo que crea un ambiente maravillosamente relajado.'},
 'tm_d2':{'en':'Cinematic elopement films that hold the movement, the sound and the feeling of your day &mdash; a moving companion to the photographs.',
          'de':'Cineastische Elopement-Filme, die Bewegung, Klang und Gefühl eures Tages festhalten &mdash; die bewegte Ergänzung zu den Fotos.',
          'es':'Films de elopement cinematográficos que capturan el movimiento, el sonido y la emoción de vuestro día &mdash; el complemento en movimiento a las fotografías.'},
 'tm_d3':{'en':'Natural, long-lasting bridal hair &amp; make-up built for wind, altitude and first light on the mountain &mdash; you, at your most radiant.',
          'de':'Natürliches, langanhaltendes Braut-Make-up &amp; Haarstyling für Wind, Höhe und erstes Licht am Berg &mdash; ihr, im schönsten Licht.',
          'es':'Peluquería y maquillaje nupcial natural y duradero, pensado para el viento, la altura y la primera luz en la montaña &mdash; vosotras, radiantes.'},
 'tm_rp':{'en':'Photography &amp; Direction','de':'Fotografie &amp; Regie','es':'Fotografía y dirección'},
 'tm_dp':{'en':'Founder and lead photographer &mdash; Tyrolean, at home between Innsbruck and the Dolomites. Award-winning (Way Up North Awards 2024), published in Rangefinder. Andreas guides every couple to the light and frames the day as it truly feels.',
          'de':'Gründer und leitender Fotograf &mdash; Tiroler, daheim zwischen Innsbruck und den Dolomiten. Ausgezeichnet (Way Up North Awards 2024), veröffentlicht im Rangefinder. Andreas führt jedes Paar ins richtige Licht und hält den Tag so fest, wie er sich wirklich anfühlt.',
          'es':'Fundador y fotógrafo principal &mdash; tirolés, en casa entre Innsbruck y las Dolomitas. Premiado (Way Up North Awards 2024), publicado en Rangefinder. Andreas guía a cada pareja hacia la luz y captura el día tal como se siente.'},
 'bts_k':{'en':'On location','de':'Vor Ort','es':'Sobre el terreno'},
 'bts_over':{'en':'Behind the scenes','de':'Hinter den Kulissen','es':'Entre bastidores'},
 'bts_h':{'en':'With our couples,<br>in the mountains','de':'Mit unseren Paaren,<br>in den Bergen','es':'Con nuestras parejas,<br>en las montañas'},
 # hero / home
 'h_sub':{'en':'Intimate mountain weddings in the Dolomites &amp; the Alps &mdash; just the two of you, a summit, and a story worth telling.',
          'de':'Intime Berghochzeiten in den Dolomiten/Alpen &mdash; nur ihr beide, ein Gipfel und eine Geschichte, die es zu erzählen lohnt.',
          'es':'Bodas íntimas de montaña en los Dolomitas y los Alpes &mdash; solo vosotros dos, una cumbre y una historia que merece contarse.'},
 'h_btn':{'en':'Begin your story','de':'Eure Geschichte beginnen','es':'Empezad vuestra historia'},
 'h_h1':{'en':'Adventure<br>Above the Clouds','de':'Abenteuer<br>über den Wolken','es':'Aventura<br>sobre las nubes'},
 'ms1':{'en':'<b>Est.</b> Tyrol &middot; Dolomites','de':'<b>Sitz</b> Tirol &middot; Dolomiten','es':'<b>Base</b> Tirol &middot; Dolomitas'},
 'ms2':{'en':'<b>Elopement</b> Photography &amp; Film','de':'<b>Elopement</b> Fotografie &amp; Film','es':'<b>Elopement</b> Fotografía y Film'},
 'ms3':{'en':'<b>Planning</b> Fully bespoke','de':'<b>Planung</b> Individuell','es':'<b>Planificación</b> A medida'},
 'ms4':{'en':'<b>Since</b> 2019','de':'<b>Seit</b> 2019','es':'<b>Desde</b> 2019'},
 'mission_k':{'en':'Our Mission','de':'Unsere Mission','es':'Nuestra misión'},
 'mission_h':{'en':'Crafting your<br>perfect elopement','de':'Euer perfektes<br>Elopement gestalten','es':'Creamos vuestro<br>elopement perfecto'},
 'mission_lead':{'en':'<em>to elope</em> &mdash; to slip away from the ordinary and marry where the world falls <em>silent</em>.',
                 'de':'<em>to elope</em> &mdash; dem Gewöhnlichen entfliehen und dort heiraten, wo die Welt <em>still</em> wird.',
                 'es':'<em>to elope</em> &mdash; escapar de lo ordinario y casarse donde el mundo se vuelve <em>silencio</em>.'},
 'mission_p1':{'en':'We design intimate weddings that reflect your unique love story. If you want to skip the extravagance of traditional venues and long guest lists, you have found your partner. We celebrate individuality while weaving timeless romance into every elopement we create.',
               'de':'Wir gestalten intime Hochzeiten, die eure einzigartige Liebesgeschichte widerspiegeln. Wenn ihr auf große Locations und lange Gästelisten verzichten wollt, seid ihr bei uns richtig. Wir feiern Individualität und weben zeitlose Romantik in jedes Elopement.',
               'es':'Diseñamos bodas íntimas que reflejan vuestra historia de amor única. Si queréis prescindir de los grandes salones y las largas listas de invitados, habéis encontrado a vuestro socio. Celebramos la individualidad y tejemos un romanticismo atemporal en cada elopement.'},
 'mission_p2':{'en':'From crystal-clear lakes to snow-capped peaks and tranquil meadows, our handpicked locations across Europe are chosen to match your vision &mdash; and we guide you every step of the way.',
               'de':'Von kristallklaren Seen über schneebedeckte Gipfel bis zu stillen Almwiesen &mdash; unsere handverlesenen Orte in ganz Europa passen zu eurer Vision, und wir begleiten euch bei jedem Schritt.',
               'es':'Desde lagos cristalinos hasta cumbres nevadas y prados tranquilos, nuestros lugares seleccionados por toda Europa se eligen para vuestra visión &mdash; y os acompañamos en cada paso.'},
 'mission_link':{'en':'How it works &rarr;','de':'So funktioniert&rsquo;s &rarr;','es':'Cómo funciona &rarr;'},
 'cap_seceda':{'en':'Sunrise on the Seceda ridge, South Tyrol.','de':'Sonnenaufgang am Seceda-Grat, Südtirol.','es':'Amanecer en la cresta del Seceda, Tirol del Sur.'},
 'sel_k':{'en':'Selected Work','de':'Ausgewählte Arbeiten','es':'Trabajos seleccionados'},
 'sel_h':{'en':'Recent stories','de':'Aktuelle Stories','es':'Historias recientes'},
 'fig1':{'en':'Elopements','de':'Elopements','es':'Elopements'},
 'fig2':{'en':'Ceremonies','de':'Zeremonien','es':'Ceremonias'},
 'fig3':{'en':'m above sea level','de':'m über dem Meer','es':'m sobre el mar'},
 'fig4':{'en':'Cups of coffee','de':'Tassen Kaffee','es':'Tazas de café'},
 'kw_k':{'en':'Kind Words','de':'Kundenstimmen','es':'Testimonios'},
 'kw_q':{'en':'"Their local knowledge was invaluable. They recommended the perfect summit and made our magical day truly unforgettable."',
         'de':'"Ihr lokales Wissen war unbezahlbar. Sie empfahlen den perfekten Gipfel und machten unseren magischen Tag wirklich unvergesslich."',
         'es':'"Su conocimiento local fue inestimable. Nos recomendaron la cumbre perfecta e hicieron de nuestro día mágico algo verdaderamente inolvidable."'},
 'kw_who':{'en':'Aubrey &amp; Matt &mdash; Dolomites, 2024','de':'Aubrey &amp; Matt &mdash; Dolomiten, 2024','es':'Aubrey y Matt &mdash; Dolomitas, 2024'},
 'cta_k':{'en':'Get in touch','de':'Kontakt','es':'Contacto'},
 'cta_h':{'en':'Your adventure is<br>a conversation away','de':'Euer Abenteuer ist nur<br>ein Gespräch entfernt','es':'Vuestra aventura está<br>a una conversación'},
 # what makes us different
 'diff_k':{'en':'Why us','de':'Warum wir','es':'Por qué nosotros'},
 'diff_h':{'en':'What makes us different','de':'Was uns unterscheidet','es':'Lo que nos hace diferentes'},
 'diff1_h':{'en':'Full-service, truly full','de':'Full-Service, wirklich komplett','es':'Full-service, de verdad completo'},
 'diff1_p':{'en':'Planning, permits, flowers, cake, ceremony, photography and film &mdash; one local team, one point of contact. You arrive, we have taken care of everything else.',
            'de':'Planung, Genehmigungen, Blumen, Torte, Zeremonie, Foto und Film &mdash; ein lokales Team, ein Ansprechpartner. Ihr kommt an, um alles andere haben wir uns gekümmert.',
            'es':'Planificación, permisos, flores, tarta, ceremonia, fotografía y vídeo &mdash; un equipo local, un único contacto. Vosotros llegáis, de todo lo demás nos hemos ocupado nosotros.'},
 'diff2_h':{'en':'Epic without the climb','de':'Episch ohne den Aufstieg','es':'Épico sin la subida'},
 'diff2_p':{'en':'From helicopter elopements above the Dolomites to hand-picked locations reachable by cable car: we create breathtaking days for couples who want the summit feeling &mdash; with or without the six-hour hike.',
            'de':'Vom Helikopter-Elopement über den Dolomiten bis zu handverlesenen Orten, die mit der Seilbahn erreichbar sind: Wir schaffen atemberaubende Tage für Paare, die das Gipfelgefühl wollen &mdash; mit oder ohne sechsstündige Wanderung.',
            'es':'Desde elopements en helicóptero sobre las Dolomitas hasta lugares escogidos accesibles en teleférico: creamos días de ensueño para parejas que quieren la sensación de cumbre &mdash; con o sin la caminata de seis horas.'},
 'diff3_h':{'en':'Legally married, right on the mountain','de':'Rechtsgültig heiraten, direkt am Berg','es':'Casados legalmente, en plena montaña'},
 'diff3_p':{'en':'As Austrians, we know how to make your mountain wedding legally binding &mdash; with a registrar at the summit. Real ceremony, real certificate, real mountains. (Symbolic ceremonies in the Italian Dolomites, of course, are just as beautiful.)',
            'de':'Als Österreicher wissen wir, wie eure Berghochzeit rechtsgültig wird &mdash; mit einem Standesbeamten am Gipfel. Echte Zeremonie, echte Urkunde, echte Berge. (Symbolische Zeremonien in den italienischen Dolomiten sind natürlich genauso schön.)',
            'es':'Como austriacos, sabemos cómo hacer que vuestra boda de montaña sea legalmente válida &mdash; con un oficial del registro en la cumbre. Ceremonia real, certificado real, montañas reales. (Las ceremonias simbólicas en las Dolomitas italianas son, por supuesto, igual de bonitas.)'},
 'diff4_h':{'en':'Born here, at home here','de':'Hier geboren, hier zu Hause','es':'Nacidos aquí, en casa aquí'},
 'diff4_p':{'en':'A small, local team at home between Innsbruck and the Dolomites &mdash; planner Jlenia, photographer Andreas and filmmaker Stefanie. Award-winning: Way Up North Awards 2024.',
            'de':'Ein kleines, lokales Team, daheim zwischen Innsbruck und den Dolomiten &mdash; Plannerin Jlenia, Fotograf Andreas und Filmerin Stefanie. Ausgezeichnet: Way Up North Awards 2024.',
            'es':'Un equipo pequeño y local, en casa entre Innsbruck y las Dolomitas &mdash; la planner Jlenia, el fotógrafo Andreas y la filmmaker Stefanie. Premiados: Way Up North Awards 2024.'},
 'award_lbl':{'en':'Awarded','de':'Ausgezeichnet','es':'Premiados'},
 'pub_lbl':{'en':'Published in','de':'Veröffentlicht in','es':'Publicado en'},
 'aw_k':{'en':'Recognition','de':'Anerkennung','es':'Reconocimiento'},
 'aw_h':{'en':'Awarded &amp; Featured','de':'Ausgezeichnet &amp; vorgestellt','es':'Premiados y destacados'},
 'aw_lead':{'en':'Booking a wedding in mountains you have never set foot in takes trust. Over the years our work has been awarded and published by people whose judgement couples rely on.',
            'de':'Eine Hochzeit in Bergen zu buchen, die man noch nie betreten hat, verlangt Vertrauen. Unsere Arbeit wurde über die Jahre ausgezeichnet und veröffentlicht &mdash; von Menschen, auf deren Urteil sich Paare verlassen.',
            'es':'Reservar una boda en montañas que nunca habéis pisado exige confianza. Con los años, nuestro trabajo ha sido premiado y publicado por quienes las parejas toman como referencia.'},
 'aw_qual':{'en':'Qualification','de':'Qualifikation','es':'Cualificación'},
 'aw_feat':{'en':'Featured','de':'Vorgestellt','es':'Destacado'},
 'aw_member':{'en':'Member','de':'Mitglied','es':'Miembro'},
 'aw_wun':{'en':'Winner &mdash; Best Epic Portrait','de':'Sieger &mdash; Best Epic Portrait','es':'Ganador &mdash; Best Epic Portrait'},
 'aw_jb':{'en':'Austria&rsquo;s Best','de':'Österreichs Beste','es':'Los mejores de Austria'},
 'aw_fl':{'en':'Listed photographer','de':'Gelistetes Mitglied','es':'Fotógrafo listado'},
 'aw_rf':{'en':'Rf Photo of the Day','de':'Rf Photo of the Day','es':'Rf Photo of the Day'},
 # how to
 'ht_k':{'en':'Field Guide','de':'Ratgeber','es':'Guía'},
 'ht_h1':{'en':'How to Elope in<br>the Dolomites','de':'Elopement in<br>den Dolomiten','es':'Cómo fugarse en<br>los Dolomitas'},
 'ht_s1k':{'en':'Where to begin','de':'Wo ihr beginnt','es':'Por dónde empezar'},
 'ht_s1h':{'en':'Blend adventure<br>and romance','de':'Abenteuer und<br>Romantik verbinden','es':'Aventura y<br>romance unidos'},
 'ht_s1p1':{'en':'Curious about designing an elopement that seamlessly blends adventure and romance in the breathtaking Dolomites? Our expertise lies in curating unforgettable mountain elopements tailored to your unique vision and preferences.',
            'de':'Neugierig auf ein Elopement, das Abenteuer und Romantik in den atemberaubenden Dolomiten vereint? Unsere Stärke ist es, unvergessliche Berghochzeiten ganz nach eurer Vision zu gestalten.',
            'es':'Imagináis un elopement que una aventura y romance en los impresionantes Dolomitas. Nuestra especialidad es crear elopements de montaña inolvidables, hechos a la medida de vuestra visión.'},
 'ht_s1p2':{'en':'We begin by helping you select the perfect mountain location &mdash; considering accessibility, scenery, and the mood you desire. Whether you dream of exchanging vows on a secluded peak or beside a tranquil alpine lake, every detail is shaped around the two of you.',
            'de':'Wir beginnen damit, den perfekten Ort für euch zu finden &mdash; nach Erreichbarkeit, Landschaft und Stimmung. Ob Gipfel oder stiller Bergsee, jedes Detail dreht sich um euch beide.',
            'es':'Empezamos ayudándoos a elegir el lugar perfecto &mdash; según accesibilidad, paisaje y ambiente. Ya soñéis con daros el sí en una cumbre apartada o junto a un lago alpino, cada detalle gira en torno a vosotros dos.'},
 'ht_s1p3':{'en':f'When the day calls for more hands, we work with a trusted circle: on-the-ground planning by <a class="partner-inline" href="{P_PLAN[1]}" target="_blank" rel="noopener">Dolomites Wedding Planner</a>, photography by <a class="partner-inline" href="https://hochzeitsfotograf.tirol" target="_blank" rel="noopener">Blitzkneisser</a>.',
            'de':f'Wenn der Tag mehr Hände braucht, arbeiten wir mit einem festen Kreis: Planung vor Ort durch <a class="partner-inline" href="{P_PLAN[1]}" target="_blank" rel="noopener">Dolomites Wedding Planner</a>, Fotografie durch <a class="partner-inline" href="https://hochzeitsfotograf.tirol" target="_blank" rel="noopener">Blitzkneisser</a>.',
            'es':f'Cuando el día pide más manos, trabajamos con un círculo de confianza: planificación sobre el terreno por <a class="partner-inline" href="{P_PLAN[1]}" target="_blank" rel="noopener">Dolomites Wedding Planner</a>, fotografía por <a class="partner-inline" href="https://hochzeitsfotograf.tirol" target="_blank" rel="noopener">Blitzkneisser</a>.'},
 'ht_cap':{'en':'A quiet morning above the tree line.','de':'Ein stiller Morgen oberhalb der Baumgrenze.','es':'Una mañana tranquila por encima de la línea de árboles.'},
 'ht_e_k':{'en':'The essentials','de':'Das Wesentliche','es':'Lo esencial'},
 'ht_e_h':{'en':'What to consider','de':'Was zu bedenken ist','es':'Qué tener en cuenta'},
 'ht_step1t':{'en':'Choose the location','de':'Den Ort wählen','es':'Elegir el lugar'},
 'ht_step1p':{'en':'Peak, lake, meadow or ridge &mdash; we match the setting to your vision, the season, and how far you want to walk.',
              'de':'Gipfel, See, Wiese oder Grat &mdash; wir wählen den Ort nach eurer Vision, der Jahreszeit und der gewünschten Gehstrecke.',
              'es':'Cumbre, lago, prado o cresta &mdash; elegimos el escenario según vuestra visión, la estación y cuánto queréis caminar.'},
 'ht_step2t':{'en':'Plan the day','de':'Den Tag planen','es':'Planear el día'},
 'ht_step2p':{'en':'A relaxed timeline, the best light, a flexible weather plan, and every logistic handled &mdash; transfers, flowers, hair &amp; make-up.',
              'de':'Ein entspannter Ablauf, das beste Licht, ein flexibler Wetterplan und alle Logistik &mdash; Transfers, Blumen, Hair &amp; Make-up.',
              'es':'Un plan relajado, la mejor luz, un plan flexible para el clima y toda la logística &mdash; traslados, flores, peluquería y maquillaje.'},
 'ht_step3t':{'en':'Say your vows','de':'Das Ja-Wort','es':'Vuestros votos'},
 'ht_step3p':{'en':'Personal vows, an optional celebrant or civil ceremony, and photography that captures it exactly as it felt.',
              'de':'Persönliche Gelübde, auf Wunsch freie oder standesamtliche Trauung, und Fotos, die alles genau so festhalten, wie es sich anfühlte.',
              'es':'Votos personales, un oficiante o ceremonia civil opcional, y una fotografía que lo captura tal como se sintió.'},
 'ht_ready':{'en':'Let\'s begin','de':'Los geht&rsquo;s','es':'Empecemos'},
 'ht_cta_h':{'en':'Let\'s start planning<br>your mountain escape','de':'Planen wir eure<br>Flucht in die Berge','es':'Empecemos a planear<br>vuestra escapada a la montaña'},
 # stories index
 'st_k':{'en':'The Archive','de':'Das Archiv','es':'El archivo'},
 'st_h':{'en':'Stories','de':'Stories','es':'Historias'},
 'st_lead':{'en':'An insight into the adventures we\'ve had the honour of capturing &mdash; vows on summits, first light on the ridges, and quiet moments above the clouds.',
            'de':'Ein Einblick in die Abenteuer, die wir festhalten durften &mdash; Gelübde auf Gipfeln, erstes Licht auf den Graten und stille Momente über den Wolken.',
            'es':'Una mirada a las aventuras que hemos tenido el honor de capturar &mdash; votos en las cumbres, la primera luz en las crestas y momentos de calma sobre las nubes.'},
 'st_cta_k':{'en':'Your story','de':'Eure Geschichte','es':'Vuestra historia'},
 'st_cta_h':{'en':'Could the next one<br>be yours?','de':'Wird die nächste<br>eure sein?','es':'¿Será vuestra<br>la próxima?'},
 # category
 'cat_k':{'en':'Category','de':'Kategorie','es':'Categoría'},
 'cat_lead':{'en':'Elopement stories filed under <em>{x}</em>.','de':'Elopement-Stories in der Kategorie <em>{x}</em>.','es':'Historias de elopement en la categoría <em>{x}</em>.'},
 # portfolio item
 'pi_lead':{'en':'A single day, start to finish &mdash; the approach, the light, the quiet exchange of vows, and the long walk back down.',
            'de':'Ein einziger Tag, von Anfang bis Ende &mdash; der Aufstieg, das Licht, das stille Ja-Wort und der lange Weg hinab.',
            'es':'Un solo día, de principio a fin &mdash; la subida, la luz, el sereno intercambio de votos y el largo camino de regreso.'},
 'pi_p':{'en':'Here is their morning above the clouds, exactly as it unfolded.',
         'de':'Hier ist ihr Morgen über den Wolken, genau so, wie er sich entfaltet hat.',
         'es':'Aquí está su mañana sobre las nubes, tal y como sucedió.'},
 'pi_gallery':{'en':'The day in frames','de':'Der Tag in Bildern','es':'El día en imágenes'},
 'pi_outro':{'en':'However you picture your day &mdash; a quiet sunrise, a summit, a lake to yourselves &mdash; we plan it around the two of you and photograph it the way it truly felt.',
             'de':'Wie auch immer ihr euch euren Tag vorstellt &mdash; ein stiller Sonnenaufgang, ein Gipfel, ein See für euch allein &mdash; wir planen ihn um euch beide und fotografieren ihn so, wie er sich wirklich angefühlt hat.',
             'es':'Sea como sea que imaginéis vuestro día &mdash; un amanecer tranquilo, una cumbre, un lago para vosotros &mdash; lo planificamos en torno a los dos y lo fotografiamos tal como se sintió.'},
 'pi_your':{'en':'Dreaming of this?','de':'Träumt ihr davon?','es':'¿Lo soñáis?'},
 'pi_cta_h':{'en':'Let\'s find<br>your summit','de':'Finden wir<br>euren Gipfel','es':'Encontremos<br>vuestra cumbre'},
 'pi_vplan':{'en':'Planning','de':'Planung','es':'Planificación'},
 'pi_vfilm':{'en':'Film','de':'Film','es':'Film'},
 'pi_vmua':{'en':'Make-up','de':'Make-up','es':'Maquillaje'},
 # packages
 'pk_k':{'en':'Investment','de':'Investition','es':'Inversión'},
 'pk_h':{'en':'Price List','de':'Preise','es':'Precios'},
 'pk_lead':{'en':'Our packages are a starting point, not a limit. Whether you dream of a three-day helicopter wedding or a simple mountaintop ceremony &mdash; only the sky is our limit.',
            'de':'Unsere Pakete sind ein Startpunkt, keine Grenze. Ob dreitägige Hubschrauber-Hochzeit oder schlichte Zeremonie am Gipfel &mdash; nur der Himmel ist unsere Grenze.',
            'es':'Nuestros paquetes son un punto de partida, no un límite. Ya soñéis con una boda de tres días en helicóptero o una sencilla ceremonia en la cima &mdash; solo el cielo es el límite.'},
 'pk_t1':{'en':'express elopement','de':'express elopement','es':'express elopement'},
 'pk_t2':{'en':'the elopement','de':'the elopement','es':'the elopement'},
 'pk_t3':{'en':'micro wedding','de':'micro wedding','es':'micro wedding'},
 'pk_l1':{'en':'Basic','de':'Basis','es':'Básico'},
 'pk_l2':{'en':'Popular','de':'Beliebt','es':'Popular'},
 'pk_l3':{'en':'Everything','de':'Alles','es':'Todo'},
 'pk_hours':{'en':'hours of coverage','de':'Stunden Begleitung','es':'horas de cobertura'},
 'pk_photos':{'en':'photos','de':'Fotos','es':'fotos'},
 'pk_note':{'en':f'Full planning &amp; on-the-ground coordination is delivered together with our partner <a class="partner-inline" href="{P_PLAN[1]}" target="_blank" rel="noopener">Dolomites Wedding Planner</a> &mdash; Mountain Elopement remains your single point of contact.',
            'de':f'Vollständige Planung &amp; Koordination vor Ort erfolgt gemeinsam mit unserem Partner <a class="partner-inline" href="{P_PLAN[1]}" target="_blank" rel="noopener">Dolomites Wedding Planner</a> &mdash; Mountain Elopement bleibt eure zentrale Ansprechstelle.',
            'es':f'La planificación completa y la coordinación sobre el terreno se realizan junto a nuestro socio <a class="partner-inline" href="{P_PLAN[1]}" target="_blank" rel="noopener">Dolomites Wedding Planner</a> &mdash; Mountain Elopement sigue siendo vuestro único punto de contacto.'},
 'pk_addk':{'en':'Can it be something special?','de':'Darf es etwas Besonderes sein?','es':'¿Algo aún más especial?'},
 'pk_cta_h':{'en':'Build your bespoke<br>elopement package','de':'Stellt euer individuelles<br>Elopement-Paket zusammen','es':'Cread vuestro paquete<br>de elopement a medida'},
 'pk_req_price':{'en':'Request pricing','de':'Preise anfragen','es':'Solicitar precios'},
 'pk_band_k':{'en':'How we work','de':'Wie wir arbeiten','es':'Cómo trabajamos'},
 'pk_band_q':{'en':'"Our pricing is a glimpse into what\'s possible. Every couple has their own vision and budget &mdash; so we tailor each package to suit your specific desires."',
              'de':'"Unsere Preise sind ein Blick auf das Mögliche. Jedes Paar hat eigene Vorstellungen und ein eigenes Budget &mdash; deshalb passen wir jedes Paket individuell an."',
              'es':'"Nuestros precios son una muestra de lo posible. Cada pareja tiene su propia visión y presupuesto &mdash; por eso adaptamos cada paquete a vuestros deseos."'},
 'pk_next':{'en':'Let\'s plan','de':'Planen wir','es':'Planeemos'},
 # add-on names
 'ad_heli':{'en':'Helicopter','de':'Hubschrauber','es':'Helicóptero'},
 'ad_film':{'en':'Film &middot; 1&ndash;2 min','de':'Film &middot; 1&ndash;2 Min','es':'Film &middot; 1&ndash;2 min'},
 'ad_civil':{'en':'Civil ceremony','de':'Standesamt','es':'Ceremonia civil'},
 'ad_celeb':{'en':'Celebrant','de':'Freie Trauung','es':'Oficiante'},
 'ad_cake':{'en':'Cake','de':'Torte','es':'Tarta'},
 'ad_music':{'en':'Musicians','de':'Musiker','es':'Músicos'},
 'ad_mua':{'en':'Hair &amp; Make-up','de':'Hair &amp; Make-up','es':'Peluquería y maquillaje'},
 'ad_backdrop':{'en':'Backdrop &amp; flowers','de':'Backdrop &amp; Blumen','es':'Backdrop y flores'},
 'ad_from':{'en':'from','de':'ab','es':'desde'},
 'ad_onreq':{'en':'on request','de':'auf Anfrage','es':'a consulta'},
 # team page
 'tp_k':{'en':'The People','de':'Die Menschen','es':'Las personas'},
 'tp_h':{'en':'Our Team','de':'Unser Team','es':'Nuestro equipo'},
 'tp_lead':{'en':'A mountain elopement takes a small, trusted circle. Here are the people who make your day happen &mdash; from the first frame to the final detail.',
            'de':'Ein Berg-Elopement braucht einen kleinen, vertrauten Kreis. Das sind die Menschen, die euren Tag möglich machen &mdash; vom ersten Bild bis zum letzten Detail.',
            'es':'Un elopement de montaña necesita un círculo pequeño y de confianza. Estas son las personas que hacen posible vuestro día &mdash; desde la primera toma hasta el último detalle.'},
 'tp_fk':{'en':'The core team','de':'Das Kernteam','es':'El equipo principal'},
 'tp_flead':{'en':'Mountain Elopement &mdash; a small local team behind your day.','de':'Mountain Elopement &mdash; ein kleines lokales Team hinter eurem Tag.','es':'Mountain Elopement &mdash; un pequeño equipo local detrás de vuestro día.'},
 'tp_fp1':{'en':'We are a small, local team at home in the Dolomites and the Alps &mdash; led by planner Jlenia and photographer Andreas. For years we have guided couples to quiet summits and hidden lakes, capturing the day exactly as it feels &mdash; unposed, unhurried, real.',
           'de':'Wir sind ein kleines, lokales Team, zu Hause in den Dolomiten/Alpen &mdash; angeführt von Plannerin Jlenia und Fotograf Andreas. Seit Jahren führen wir Paare zu stillen Gipfeln und versteckten Seen und halten den Tag genau so fest, wie er sich anfühlt &mdash; ungestellt, unhektisch, echt.',
           'es':'Somos un equipo pequeño y local, en casa en los Dolomitas y los Alpes &mdash; encabezado por la planner Jlenia y el fotógrafo Andreas. Durante años hemos guiado a parejas hasta cumbres silenciosas y lagos escondidos, capturando el día tal como se siente &mdash; sin poses, sin prisas, real.'},
 'tp_fp2':{'en':'Between us we plan and photograph your whole day &mdash; and where it makes your day even better, we bring in a trusted circle around us.',
           'de':'Gemeinsam planen und fotografieren wir euren ganzen Tag &mdash; und wo es euren Tag noch schöner macht, holen wir einen vertrauten Kreis dazu.',
           'es':'Juntos planificamos y fotografiamos vuestro día entero &mdash; y donde lo mejora aún más, sumamos un círculo de confianza.'},
 'tp_hello':{'en':'Say hello &rarr;','de':'Hallo sagen &rarr;','es':'Saludad &rarr;'},
 'tp_cta_k':{'en':'One team','de':'Ein Team','es':'Un equipo'},
 'tp_cta_h':{'en':'Everything you need,<br>from one hand','de':'Alles aus einer Hand','es':'Todo lo que necesitáis,<br>de una sola mano'},
 'tp_plan':{'en':'Plan your day','de':'Euren Tag planen','es':'Planear vuestro día'},
 # contact
 'ct_k':{'en':'Say hello','de':'Sagt Hallo','es':'Saludad'},
 'ct_h':{'en':'Get in Touch','de':'Kontakt','es':'Contacto'},
 'ct_lead':{'en':'We are looking forward to hearing your story! Tell us your ideas &mdash; and we\'ll help turn your dream elopement into reality.',
            'de':'Wir freuen uns auf eure Geschichte! Erzählt uns eure Ideen &mdash; und wir machen euer Traum-Elopement wahr.',
            'es':'¡Estamos deseando escuchar vuestra historia! Contadnos vuestras ideas &mdash; y os ayudaremos a hacer realidad vuestro elopement soñado.'},
 'ct_details':{'en':'Your details','de':'Eure Angaben','es':'Vuestros datos'},
 'ct_name':{'en':'Name','de':'Name','es':'Nombre'},
 'ct_name_ph':{'en':'Your name','de':'Euer Name','es':'Vuestro nombre'},
 'ct_email':{'en':'Email','de':'E-Mail','es':'Correo'},
 'ct_date':{'en':'Elopement date (approx.)','de':'Elopement-Datum (ca.)','es':'Fecha del elopement (aprox.)'},
 'ct_date_ph':{'en':'e.g. June 2027','de':'z. B. Juni 2027','es':'p. ej. junio 2027'},
 'ct_dream':{'en':'What are you dreaming of?','de':'Wovon träumt ihr?','es':'¿Con qué soñáis?'},
 'ct_story':{'en':'Tell us your story','de':'Erzählt uns eure Geschichte','es':'Contadnos vuestra historia'},
 'ct_story_ph':{'en':'Where, when, and what you\'re imagining...','de':'Wo, wann und was ihr euch vorstellt...','es':'Dónde, cuándo y qué imagináis...'},
 'ct_send':{'en':'Send enquiry','de':'Anfrage senden','es':'Enviar consulta'},
 'ct_sending':{'en':'Sending…','de':'Wird gesendet…','es':'Enviando…'},
 'ct_ok':{'en':'Sent — thank you!','de':'Gesendet — danke!','es':'¡Enviado, gracias!'},
 'ct_err':{'en':'Something went wrong. Please try again or email us directly.','de':'Etwas ist schiefgelaufen. Bitte erneut versuchen oder schreibt uns direkt.','es':'Algo salió mal. Inténtalo de nuevo o escríbenos directamente.'},
 'ct_note':{'en':'Prototype form &mdash; in the live version this connects to email (e.g. Formspree).',
            'de':'Prototyp-Formular &mdash; in der Live-Version verbunden mit E-Mail (z. B. Formspree).',
            'es':'Formulario prototipo &mdash; en la versión final se conecta al correo (p. ej. Formspree).'},
 'ct_based':{'en':'Based in','de':'Sitz','es':'Base'},
 'ct_based_v':{'en':'Tyrol &amp; the Dolomites','de':'Tirol &amp; Dolomiten','es':'Tirol y los Dolomitas'},
 # thank-you (noindex confirmation page)
 'ty_k':{'en':'Enquiry received','de':'Anfrage erhalten','es':'Consulta recibida'},
 'ty_h':{'en':'Thank you','de':'Danke','es':'Gracias'},
 'ty_p':{'en':'We\u2019ve received your message and will get back to you within 48 hours.',
         'de':'Wir haben eure Nachricht erhalten und melden uns innerhalb von 48 Stunden.',
         'es':'Hemos recibido vuestro mensaje y os responderemos en un plazo de 48 horas.'},
 'ty_home':{'en':'Back to homepage','de':'Zur\u00fcck zur Startseite','es':'Volver al inicio'},
 # chips
 'chips':{'en':['Photo','Film','Backdrop','Flowers','Make-up','Helicopter','Hike','Musician'],
          'de':['Foto','Film','Backdrop','Blumen','Make-up','Hubschrauber','Wanderung','Musik'],
          'es':['Foto','Film','Backdrop','Flores','Maquillaje','Helicóptero','Senderismo','Música']},
 # legal
 'lg_k':{'en':'Legal','de':'Rechtliches','es':'Legal'},
 'lg_imprint':{'en':'Imprint','de':'Impressum','es':'Aviso legal'},
 'lg_privacy':{'en':'Privacy Policy','de':'Datenschutz','es':'Política de privacidad'},
 'lg_lead':{'en':'Placeholder &mdash; the existing text will be carried over unchanged from the current site.',
            'de':'Platzhalter &mdash; der bestehende Text wird unverändert von der aktuellen Seite übernommen.',
            'es':'Marcador de posición &mdash; el texto existente se trasladará sin cambios desde el sitio actual.'},
 # guides
 'hero_inq':{'en':'Direct inquiry','de':'Direkt anfragen','es':'Consulta directa'},
 'hero_guides':{'en':'Guides','de':'Guides','es':'Guías'},
 'hero_price':{'en':'Price list','de':'Preise','es':'Precios'},
 'film_k':{'en':'The film','de':'Der Film','es':'El vídeo'},
 'gd_k':{'en':'The field guide','de':'Der Guide','es':'La guía'},
 'gd_h':{'en':'Guides','de':'Guides','es':'Guías'},
 'ht_start':{'en':'Start Here','de':'Hier starten','es':'Empieza aquí'},
 'ht_start_copy':{'en':'A calm starting point for couples planning a Dolomites elopement or an intentional wedding in the mountains &mdash; and wanting a clearer sense of where to begin.',
                  'de':'Ein ruhiger Startpunkt für Paare, die ein Dolomiten-Elopement oder eine bewusste Hochzeit in den Bergen planen &mdash; und einen klaren Überblick suchen, wo sie beginnen.',
                  'es':'Un punto de partida sereno para parejas que planean un elopement en los Dolomitas o una boda con intención en la montaña &mdash; y quieren una idea más clara de por dónde empezar.'},
 'guides_k':{'en':'Planning Guides','de':'Planungs-Guides','es':'Guías de planificación'},
 'guides_h':{'en':'Elopement planning guides','de':'Elopement-Planungs-Guides','es':'Guías para planear tu elopement'},
 'guides_intro':{'en':'Practical, honest guides to help you plan an elopement in the Alps and Dolomites.',
                 'de':'Praktische, ehrliche Guides für euer Elopement in Alpen und Dolomiten.',
                 'es':'Guías prácticas y honestas para planear vuestro elopement en los Alpes y los Dolomitas.'},
 'read_guide':{'en':'Read guide','de':'Guide lesen','es':'Leer guía'},
 'guide_kick':{'en':'Guide','de':'Guide','es':'Guía'},
 'more_guides':{'en':'More guides','de':'Weitere Guides','es':'Más guías'},
 'map_k':{'en':'The region','de':'Die Region','es':'La región'},
 'map_h':{'en':'Where will you elope?','de':'Wo wollt ihr heiraten?','es':'¿Dónde os fugaréis?'},
 'map_hint':{'en':'Tap a region','de':'Region antippen','es':'Toca una región'},
 'map_tyrol':{'en':'Tyrol','de':'Tirol','es':'Tirol'},
 'map_lakes':{'en':'Alpine Lakes','de':'Bergseen','es':'Lagos alpinos'},
 'map_dol':{'en':'Dolomites','de':'Dolomiten','es':'Dolomitas'},
 'cats_k':{'en':'By theme','de':'Nach Thema','es':'Por tema'},
 'cats_h':{'en':'Explore by category','de':'Nach Kategorie entdecken','es':'Explorar por categoría'},
 'quick_facts':{'en':'At a glance','de':'Auf einen Blick','es':'De un vistazo'},
 'good_to_know':{'en':'Good to know','de':'Gut zu wissen','es':'Bueno saber'},
 'related_stories':{'en':'Real elopements','de':'Passende Stories','es':'Elopements reales'},
}
def t(lang,key): return T[key][lang]

# reusable fact labels
LBL={'season':{'en':'Best season','de':'Beste Zeit','es':'Mejor época'},
 'diff':{'en':'Difficulty','de':'Anspruch','es':'Dificultad'},
 'reach':{'en':'Getting there','de':'Anreise','es':'Cómo llegar'},
 'regions':{'en':'Regions','de':'Regionen','es':'Regiones'},
 'access':{'en':'Access','de':'Zugang','es':'Acceso'},
 'light':{'en':'Best light','de':'Bestes Licht','es':'Mejor luz'},
 'lead':{'en':'Lead time','de':'Vorlauf','es':'Antelación'},
 'guests':{'en':'Guests','de':'Gäste','es':'Invitados'},
 'includes':{'en':'Includes','de':'Enthält','es':'Incluye'}}

# story titles / category names
CATS = {'couple':{'en':'Couple','de':'Paare','es':'Parejas'},
        'dolomites':{'en':'Dolomites','de':'Dolomiten','es':'Dolomitas'},
        'mountain':{'en':'Mountain','de':'Berge','es':'Montaña'},
        'lake':{'en':'Lake','de':'Seen','es':'Lago'},
        'elopement':{'en':'Elopement','de':'Elopement','es':'Elopement'},
        'engagement':{'en':'Engagement','de':'Verlobung','es':'Compromiso'}}
def catname(slug,lang): return CATS[slug][lang]

# (num, slug, imgnum, [cats], {lang:title})
STORIES = [
 (1,'climbing-wedding','s01',['dolomites','mountain','couple'],{'en':'Mountain Peaks Climbing Wedding in the Dolomites','de':'Kletterhochzeit auf den Gipfeln der Dolomiten','es':'Boda de escalada en las cumbres de los Dolomitas'}),
 (2,'sunrise-elopement-in-the-dolomites','s02',['dolomites','elopement','mountain'],{'en':'A Magical Sunrise Elopement in the Dolomites','de':'Eine magische Sonnenaufgangs-Hochzeit in den Dolomiten','es':'Una mágica boda al amanecer en los Dolomitas'}),
 (3,'mountain-engagement','s03',['couple','engagement','mountain','lake','dolomites'],{'en':'A Peak Proposal &mdash; Mountainous Engagement','de':'Antrag am Gipfel &mdash; Verlobung in den Bergen','es':'Pedida en la cumbre &mdash; compromiso en la montaña'}),
 (4,'crystal-clear-water-elopement','s04',['dolomites','elopement','mountain','lake'],{'en':'Mountain Elopement by Crystal Waters','de':'Berghochzeit am kristallklaren Wasser','es':'Boda de montaña junto a aguas cristalinas'}),
 (5,'hiking-elopement-lagazuoi-dolomites','s05',['dolomites','elopement','mountain'],{'en':'A Winter Wedding in Val Gardena','de':'Winterhochzeit in Gröden','es':'Una boda de invierno en Val Gardena'}),
 (6,'pizza-elopement-at-tre-cime-cadini-di-misurina','s06',['dolomites','elopement','mountain'],{'en':'Pizza Elopement at Tre Cime','de':'Pizza-Hochzeit an den Drei Zinnen','es':'Boda con pizza en las Tre Cime'}),
 (7,'mountain-elopement-dolomiten','s07',['dolomites','elopement','mountain'],{'en':'Dolomites Elopement with Three Locations','de':'Dolomiten-Hochzeit an drei Orten','es':'Boda en los Dolomitas en tres lugares'}),
 (8,'sunrise-dolomites-elopement','s08',['dolomites','elopement','mountain'],{'en':'Sunrise in the Dolomites','de':'Sonnenaufgang in den Dolomiten','es':'Amanecer en los Dolomitas'}),
 (9,'official-married-in-the-alps','s09',['elopement','mountain'],{'en':'Official Elopement on Top of Tyrol','de':'Standesamtlich heiraten auf Tirols Gipfel','es':'Boda oficial en la cima del Tirol'}),
 (10,'ultimate-italian-elopement','s10',['elopement'],{'en':'An Elopement Over Three Days','de':'Eine Hochzeit über drei Tage','es':'Una boda de tres días'}),
 (11,'adventure-helicopter-elopement-dolomites','s11',['elopement','dolomites'],{'en':'Adventure Helicopter Elopement in the Dolomites','de':'Abenteuer-Hubschrauber-Hochzeit in den Dolomiten','es':'Boda de aventura en helicóptero en los Dolomitas'}),
 (12,'lake-elopement-tyrol-mountains','s12',['elopement','lake'],{'en':'Elopement at the Lake','de':'Hochzeit am See','es':'Boda junto al lago'}),
 (13,'a-journey-of-love-and-adventure','s13',['elopement','dolomites','mountain'],{'en':'A Winter Ski Elopement in the Dolomites','de':'Winter-Ski-Elopement in den Dolomiten','es':'Un elopement de esquí invernal en los Dolomitas'}),
 (14,'couple-shoot-photo','s14',['couple'],{'en':'Couple Shoot in the Autumn','de':'Paar-Shooting im Herbst','es':'Sesión de pareja en otoño'}),
 (15,'sunset-elopement-tyrol','s15',['elopement','mountain'],{'en':'Mountain-Top Sunset Elopement','de':'Sonnenuntergangs-Hochzeit am Gipfel','es':'Boda al atardecer en la cumbre'}),
 (16,'intimate-lake-eibsee-elopement','s16',['elopement','lake','mountain'],{'en':'Intimate Lake Eibsee Elopement','de':'Intime Hochzeit am Eibsee','es':'Boda íntima en el lago Eibsee'}),
 (17,'lago-di-braies-elopement','s17',['elopement','lake'],{'en':'Lago di Braies Elopement','de':'Hochzeit am Pragser Wildsee','es':'Boda en el Lago di Braies'}),
 (18,'rainy-lago-di-braies-pizza-elopement','s23',['elopement','lake','dolomites'],{'en':'Wooden Boats and Lakeside Pizza &mdash; a Lago di Braies Elopement','de':'Ruderboote und Pizza am Pragser Wildsee &mdash; ein Elopement','es':'Barcas de remos y pizza en el Lago di Braies &mdash; un elopement'}),
]

# Guides (elopement-specific, distinct from the wedding-photographer site)
GUIDES = [
 {'slug':'dolomites-elopement-guide','img':'s08',
  'title':{'en':'How to Elope in the Dolomites','de':'Elopement in den Dolomiten','es':'Cómo fugarse en los Dolomitas'},
  'excerpt':{'en':'Everything you need to marry among Italy\'s most beautiful peaks.','de':'Alles, was ihr braucht, um zwischen Italiens schönsten Gipfeln zu heiraten.','es':'Todo lo que necesitáis para casaros entre las cumbres más bellas de Italia.'},
  'intro':{'en':'The Dolomites are one of Europe\'s most breathtaking places to elope — dramatic peaks, turquoise lakes and light that turns the rock pink at dawn. Here is how to make your day here effortless.',
           'de':'Die Dolomiten gehören zu den atemberaubendsten Orten Europas für ein Elopement — schroffe Gipfel, türkise Seen und Licht, das den Fels im Morgengrauen rosa färbt. So gelingt euer Tag hier mühelos.',
           'es':'Los Dolomitas son uno de los lugares más impresionantes de Europa para un elopement — cumbres dramáticas, lagos turquesa y una luz que tiñe la roca de rosa al amanecer. Así hacéis que vuestro día aquí sea sencillo.'},
  'sec':[
   {'h':{'en':'When to go','de':'Beste Reisezeit','es':'Cuándo ir'},
    'p':{'en':'Late June to September offers reliable weather and open mountain huts. For fewer crowds and golden larches, plan for late September.',
         'de':'Ende Juni bis September bietet verlässliches Wetter und geöffnete Hütten. Für weniger Trubel und goldene Lärchen plant Ende September.',
         'es':'De finales de junio a septiembre hay tiempo estable y refugios abiertos. Para menos gente y alerces dorados, planificad a finales de septiembre.'}},
   {'h':{'en':'Where to say your vows','de':'Wo ihr euer Ja-Wort gebt','es':'Dónde dar el sí'},
    'p':{'en':'From the ridges of Seceda to the shores of Lago di Braies and the Tre Cime, we help you choose a spot that matches your fitness and your vision.',
         'de':'Von den Graten der Seceda über den Pragser Wildsee bis zu den Drei Zinnen — wir helfen euch, einen Ort passend zu Kondition und Vision zu wählen.',
         'es':'Desde las crestas del Seceda hasta la orilla del Lago di Braies y las Tre Cime, os ayudamos a elegir un lugar acorde a vuestra forma física y visión.'}},
   {'h':{'en':'Making it official','de':'Rechtsgültig heiraten','es':'Hacerlo oficial'},
    'p':{'en':'You can marry legally in Italy with some paperwork in advance, or hold a symbolic ceremony and complete the legal part at home. We point you to the right path.',
         'de':'In Italien könnt ihr mit etwas Papierkram vorab rechtsgültig heiraten — oder eine symbolische Zeremonie feiern und das Rechtliche zu Hause erledigen. Wir zeigen euch den richtigen Weg.',
         'es':'Podéis casaros legalmente en Italia con algo de papeleo previo, o celebrar una ceremonia simbólica y completar la parte legal en casa. Os indicamos el camino correcto.'}},
   {'h':{'en':'Getting there: passes, toll roads &amp; cable cars','de':'Anreise: Pässe, Mautstraßen &amp; Bergbahnen','es':'Cómo llegar: puertos, peajes y teleféricos'},
    'p':{'en':'Most couples fly into Venice, Verona or Innsbruck and drive the last stretch. The great passes &mdash; Giau, Falzarego and Pordoi &mdash; are free and scenic, but two spots cost or restrict: the Tre Cime di Lavaredo toll road above Misurina (around &euro;30&ndash;45 per car in season) climbs almost to the peaks, and Lago di Braies caps summer traffic to the lake from roughly 10:00 to 16:00, so we shoot there at first light. Where the road ends a cable car often begins &mdash; Seceda above Ortisei, Lagazuoi from Passo Falzarego, Sass Pordoi from Passo Pordoi. See [[g:most-beautiful-dolomites-spots|our favourite Dolomite locations]] for where each one leads.',
         'de':'Die meisten Paare fliegen nach Venedig, Verona oder Innsbruck und fahren das letzte Stück. Die großen Pässe &mdash; Giau, Falzarego und Pordoi &mdash; sind kostenlos und traumhaft, doch zwei Orte kosten oder beschränken: die Mautstraße zu den Drei Zinnen oberhalb von Misurina (in der Saison rund 30&ndash;45&nbsp;&euro; pro Auto) führt fast bis unter die Zinnen, und der Pragser Wildsee begrenzt den Sommerverkehr zum See etwa von 10 bis 16 Uhr &mdash; deshalb fotografieren wir dort im ersten Licht. Wo die Straße endet, beginnt oft eine Bergbahn &mdash; Seceda über Ortisei, Lagazuoi ab dem Falzaregopass, Sass Pordoi ab dem Pordoipass. In [[g:most-beautiful-dolomites-spots|unseren liebsten Dolomiten-Orten]] steht, wohin jede führt.',
         'es':'La mayoría vuela a Venecia, Verona o Innsbruck y conduce el último tramo. Los grandes puertos &mdash; Giau, Falzarego y Pordoi &mdash; son gratis y espectaculares, pero dos lugares cobran o limitan: la carretera de peaje de las Tre Cime di Lavaredo sobre Misurina (unos 30&ndash;45&nbsp;&euro; por coche en temporada) sube casi hasta las cumbres, y el Lago di Braies limita el tráfico estival al lago de 10:00 a 16:00, por eso fotografiamos allí con la primera luz. Donde acaba la carretera suele empezar un teleférico &mdash; Seceda sobre Ortisei, Lagazuoi desde el Passo Falzarego, Sass Pordoi desde el Passo Pordoi. Mirad [[g:most-beautiful-dolomites-spots|nuestros lugares favoritos de los Dolomitas]] para ver adónde lleva cada uno.'}},
   {'h':{'en':'Where to base yourselves','de':'Wo ihr euch einquartiert','es':'Dónde alojaros'},
    'p':{'en':'Cortina d\'Ampezzo, Ortisei in Val Gardena and the Alta Badia villages make the easiest bases &mdash; each within an hour of the headline locations, each full of mountain huts for a wedding-night dinner. For a dawn ceremony we often book a rifugio so you sleep on the mountain and wake already there; a real one is [[s:sunrise-dolomites-elopement|this Dolomites daybreak]], and [[g:sunrise-or-sunset-elopement|sunrise or sunset?]] helps you choose your light.',
         'de':'Cortina d\'Ampezzo, St. Ulrich (Ortisei) im Grödnertal und die Dörfer der Alta Badia sind die einfachsten Standorte &mdash; jeweils eine Stunde von den Top-Orten entfernt und voller Hütten für ein Hochzeitsdinner. Für eine Zeremonie im Morgengrauen buchen wir oft eine Hütte, damit ihr am Berg schlaft und schon dort aufwacht; ein echtes Beispiel ist [[s:sunrise-dolomites-elopement|dieser Dolomiten-Tagesanbruch]], und [[g:sunrise-or-sunset-elopement|Sonnenaufgang oder Sonnenuntergang?]] hilft bei der Wahl des Lichts.',
         'es':'Cortina d\'Ampezzo, Ortisei en Val Gardena y los pueblos de Alta Badia son las bases más cómodas &mdash; a una hora de los lugares estrella y llenos de refugios para una cena de bodas. Para una ceremonia al alba solemos reservar un rifugio para que durmáis en la montaña y despertéis ya allí; un ejemplo real es [[s:sunrise-dolomites-elopement|este amanecer en los Dolomitas]], y [[g:sunrise-or-sunset-elopement|¿amanecer o atardecer?]] os ayuda a elegir vuestra luz.'}},
  ]},
 {'slug':'elope-in-austria','img':'s01',
  'title':{'en':'How to Elope in Austria & Tyrol','de':'Elopement in Österreich & Tirol','es':'Cómo fugarse en Austria y el Tirol'},
  'excerpt':{'en':'Alpine lakes, high ridges and an easy legal marriage.','de':'Bergseen, hohe Grate und eine unkomplizierte Trauung.','es':'Lagos alpinos, crestas altas y una boda legal sencilla.'},
  'intro':{'en':'Tyrol is our home. From the peaks above Innsbruck to hidden mountain lakes, Austria makes eloping simple — and legally straightforward.',
           'de':'Tirol ist unsere Heimat. Von den Gipfeln über Innsbruck bis zu versteckten Bergseen macht Österreich ein Elopement einfach — auch rechtlich.',
           'es':'El Tirol es nuestro hogar. Desde las cumbres sobre Innsbruck hasta lagos escondidos, Austria hace que fugarse sea sencillo — también en lo legal.'},
  'sec':[
   {'h':{'en':'Legal marriage in Austria','de':'Standesamtlich in Österreich','es':'Boda legal en Austria'},
    'p':{'en':'Austria allows official ceremonies at the registry office and, in some regions, at stunning outdoor locations. We coordinate the appointment and paperwork.',
         'de':'Österreich erlaubt standesamtliche Trauungen im Amt und in manchen Regionen an traumhaften Orten im Freien. Wir koordinieren Termin und Papiere.',
         'es':'Austria permite ceremonias oficiales en el registro y, en algunas regiones, en lugares al aire libre impresionantes. Coordinamos la cita y el papeleo.'}},
   {'h':{'en':'Best locations','de':'Schönste Orte','es':'Mejores lugares'},
    'p':{'en':'The Nordkette above Innsbruck, the Zillertal, and countless alpine lakes are within easy reach.',
         'de':'Die Nordkette über Innsbruck, das Zillertal und unzählige Bergseen sind bequem erreichbar.',
         'es':'La Nordkette sobre Innsbruck, el Zillertal e innumerables lagos alpinos están a poca distancia.'}},
   {'h':{'en':'Getting there','de':'Anreise','es':'Cómo llegar'},
    'p':{'en':'Innsbruck has its own airport and fast connections to Munich and Venice, making Tyrol one of the easiest Alpine regions to reach.',
         'de':'Innsbruck hat einen eigenen Flughafen und schnelle Verbindungen nach München und Venedig — Tirol ist eine der am leichtesten erreichbaren Alpenregionen.',
         'es':'Innsbruck tiene su propio aeropuerto y conexiones rápidas con Múnich y Venecia, lo que hace del Tirol una de las regiones alpinas más accesibles.'}},
   {'h':{'en':'Cable cars &amp; alpine toll roads','de':'Bergbahnen &amp; alpine Mautstraßen','es':'Teleféricos y carreteras de peaje alpinas'},
    'p':{'en':'Innsbruck is the only city in the Alps with a high mountain on its doorstep: the Nordkette funicular and cable cars lift you from the old town to Hafelekar at 2,256&thinsp;m in about twenty minutes. Deeper in, two toll roads open turquoise water &mdash; the Schlegeis Alpine Road in the Zillertal (roughly &euro;13 per car) ends at a milky-blue reservoir, and the Kühtai and Timmelsjoch high roads climb well past the treeline. It is big Alpine scenery with almost no walking.',
         'de':'Innsbruck ist die einzige Stadt der Alpen mit einem Hochgebirge direkt vor der Tür: Die Hungerburgbahn und die Nordkettenbahnen bringen euch in rund zwanzig Minuten von der Altstadt aufs Hafelekar auf 2.256&thinsp;m. Weiter hinein öffnen zwei Mautstraßen türkises Wasser &mdash; die Schlegeis Alpenstraße im Zillertal (rund 13&nbsp;&euro; pro Auto) endet an einem milchig-blauen Stausee, und die Höhenstraßen von Kühtai und Timmelsjoch steigen weit über die Baumgrenze. Große Alpenkulisse mit fast keinem Fußweg.',
         'es':'Innsbruck es la única ciudad de los Alpes con alta montaña a la puerta: el funicular y los teleféricos de la Nordkette os suben del casco antiguo al Hafelekar, a 2.256&thinsp;m, en unos veinte minutos. Más adentro, dos carreteras de peaje abren agua turquesa &mdash; la Schlegeis Alpenstraße en el Zillertal (unos 13&nbsp;&euro; por coche) termina en un embalse azul lechoso, y las carreteras de altura de Kühtai y Timmelsjoch suben mucho más allá del bosque. Gran paisaje alpino casi sin caminar.'}},
   {'h':{'en':'Where we love to say vows in Tyrol','de':'Wo wir in Tirol das Ja am liebsten feiern','es':'Dónde nos encanta dar el sí en el Tirol'},
    'p':{'en':'Our shortlist: the protected Obernberger See near the Brenner, the emerald Schlegeisspeicher in the Zillertal, and the quiet high tarns above Kühtai. All sit close to Innsbruck yet feel a world away &mdash; see a real Tyrolean day in [[s:lake-elopement-tyrol-mountains|this alpine-lake elopement]], or, if you want it legally binding on the summit, [[s:official-married-in-the-alps|a real registrar on the mountain]]. More favourites live in [[g:best-alps-elopement-locations|our best Alpine locations]].',
         'de':'Unsere Auswahl: der geschützte Obernberger See nahe dem Brenner, der smaragdgrüne Schlegeisspeicher im Zillertal und die stillen Hochseen über Kühtai. Alle liegen nah an Innsbruck und fühlen sich doch wie eine andere Welt an &mdash; ein echter Tiroler Tag ist [[s:lake-elopement-tyrol-mountains|diese Bergsee-Hochzeit]], oder, wenn es am Gipfel rechtsgültig sein soll, [[s:official-married-in-the-alps|eine echte Standesbeamtin am Berg]]. Mehr Favoriten in [[g:best-alps-elopement-locations|unseren besten Alpen-Orten]].',
         'es':'Nuestra lista: el protegido Obernberger See junto al Brennero, el esmeralda Schlegeisspeicher en el Zillertal y las tranquilas lagunas de altura sobre Kühtai. Todos cerca de Innsbruck y a la vez en otro mundo &mdash; un día tirolés real es [[s:lake-elopement-tyrol-mountains|esta boda en un lago alpino]], o, si lo queréis legal en la cumbre, [[s:official-married-in-the-alps|un registrador de verdad en la montaña]]. Más favoritos en [[g:best-alps-elopement-locations|nuestros mejores lugares alpinos]].'}},
  ]},
 {'slug':'best-alps-elopement-locations','img':'s13',
  'title':{'en':'The Best Elopement Locations in the Alps','de':'Die schönsten Elopement-Orte in den Alpen','es':'Los mejores lugares para elopements en los Alpes'},
  'excerpt':{'en':'Our favourite peaks, lakes and meadows for an unforgettable day.','de':'Unsere liebsten Gipfel, Seen und Wiesen für einen unvergesslichen Tag.','es':'Nuestras cumbres, lagos y prados favoritos para un día inolvidable.'},
  'intro':{'en':'After years in the mountains, these are the places we return to again and again — each with its own character and light.',
           'de':'Nach Jahren in den Bergen sind das die Orte, zu denen wir immer wieder zurückkehren — jeder mit eigenem Charakter und Licht.',
           'es':'Tras años en la montaña, estos son los lugares a los que volvemos una y otra vez — cada uno con su carácter y su luz.'},
  'sec':[
   {'h':{'en':'For the peak-baggers','de':'Für Gipfelstürmer','es':'Para los amantes de las cumbres'},
    'p':{'en':'High ridges and summits for couples who want the effort — and the reward — of standing on top.',
         'de':'Hohe Grate und Gipfel für Paare, die die Anstrengung — und die Belohnung — ganz oben suchen.',
         'es':'Crestas y cumbres para parejas que buscan el esfuerzo — y la recompensa — de llegar arriba.'}},
   {'h':{'en':'For the water lovers','de':'Für Seen-Liebhaber','es':'Para los amantes del agua'},
    'p':{'en':'Turquoise alpine lakes like Braies, Eibsee and hidden Tyrolean tarns for calm, mirror-still mornings.',
         'de':'Türkise Bergseen wie der Pragser Wildsee, der Eibsee und versteckte Tiroler Bergseen für stille, spiegelglatte Morgen.',
         'es':'Lagos alpinos turquesa como Braies, Eibsee y lagunas tirolesas escondidas para mañanas serenas y espejadas.'}},
   {'h':{'en':'For the easy-going','de':'Für Genießer','es':'Para los tranquilos'},
    'p':{'en':'Gentle meadows and cable-car-accessible viewpoints when you would rather not hike far in your dress or suit.',
         'de':'Sanfte Wiesen und mit der Bergbahn erreichbare Aussichtspunkte, wenn ihr nicht weit wandern möchtet.',
         'es':'Prados suaves y miradores accesibles en teleférico cuando preferís no caminar mucho.'}},
   {'h':{'en':'Lakes worth the early start','de':'Seen, für die sich das frühe Aufstehen lohnt','es':'Lagos que merecen madrugar'},
    'p':{'en':'A few alpine lakes are worth setting an alarm for. Lago di Braies is the emerald icon with its boathouse and rowboats; Lago di Sorapis glows milky turquoise after a two-hour walk from Passo Tre Croci (no cars reach it); Lago di Federa sits in a ring of larches that turn gold in October; and the Eibsee below the Zugspitze hides wooded coves few people find. All are calmest at first light &mdash; see them in [[c:lake|our lake elopements]], including [[s:rainy-lago-di-braies-pizza-elopement|a rainy morning at Braies]].',
         'de':'Für einige Bergseen lohnt sich der Wecker. Der Pragser Wildsee ist die smaragdgrüne Ikone mit Bootshaus und Ruderbooten; der Lago di Sorapis leuchtet milchig-türkis nach zwei Stunden Weg vom Passo Tre Croci (kein Auto kommt hin); der Lago di Federa liegt in einem Kranz aus Lärchen, die im Oktober golden werden; und der Eibsee unter der Zugspitze verbirgt bewaldete Buchten, die kaum jemand findet. Alle sind im ersten Licht am ruhigsten &mdash; zu sehen in [[c:lake|unseren See-Hochzeiten]], darunter [[s:rainy-lago-di-braies-pizza-elopement|ein Regenmorgen am Pragser Wildsee]].',
         'es':'Por algunos lagos alpinos vale la pena poner el despertador. El Lago di Braies es el icono esmeralda con su caseta y sus barcas; el Lago di Sorapis brilla turquesa lechoso tras dos horas de camino desde el Passo Tre Croci (no llega ningún coche); el Lago di Federa se asienta en un anillo de alerces que se doran en octubre; y el Eibsee, bajo el Zugspitze, esconde calas boscosas que casi nadie encuentra. Todos están más tranquilos con la primera luz &mdash; miradlos en [[c:lake|nuestras bodas junto al lago]], incluida [[s:rainy-lago-di-braies-pizza-elopement|una mañana lluviosa en Braies]].'}},
   {'h':{'en':'Cable-car viewpoints without the climb','de':'Bergbahn-Aussichten ohne den Aufstieg','es':'Miradores de teleférico sin la subida'},
    'p':{'en':'If you\'d rather not hike far in a dress or suit, the lifts do the work. The Seceda cable car sets you on a tilted grass ridge above Val Gardena; Sass Pordoi &mdash; the &ldquo;terrace of the Dolomites&rdquo; &mdash; lifts you to 2,950&thinsp;m in minutes; Lagazuoi opens a balcony over half the range; and the Nordkette above Innsbruck is a twenty-minute ride from the city. We time the first or last cabin so the viewpoint is nearly empty &mdash; more on each in [[g:most-beautiful-dolomites-spots|the most beautiful Dolomite spots]].',
         'de':'Wenn ihr in Kleid oder Anzug nicht weit wandern wollt, übernehmen die Bahnen die Arbeit. Die Seceda-Bahn setzt euch auf einen geneigten Graskamm über dem Grödnertal; der Sass Pordoi &mdash; die &bdquo;Terrasse der Dolomiten&ldquo; &mdash; bringt euch in Minuten auf 2.950&thinsp;m; der Lagazuoi öffnet einen Balkon über das halbe Massiv; und die Nordkette über Innsbruck ist eine Zwanzig-Minuten-Fahrt aus der Stadt. Wir legen die erste oder letzte Gondel so, dass der Aussichtspunkt fast leer ist &mdash; mehr zu jedem in [[g:most-beautiful-dolomites-spots|den schönsten Dolomiten-Orten]].',
         'es':'Si preferís no caminar mucho con vestido o traje, los remontes hacen el trabajo. El teleférico del Seceda os deja en una cresta de hierba inclinada sobre Val Gardena; el Sass Pordoi &mdash; la &ldquo;terraza de los Dolomitas&rdquo; &mdash; os sube a 2.950&thinsp;m en minutos; el Lagazuoi abre un balcón sobre medio macizo; y la Nordkette sobre Innsbruck queda a veinte minutos de la ciudad. Programamos la primera o la última cabina para que el mirador esté casi vacío &mdash; más sobre cada uno en [[g:most-beautiful-dolomites-spots|los lugares más bellos de los Dolomitas]].'}},
  ]},
 {'slug':'how-to-plan-your-elopement','img':'s18',
  'title':{'en':'How to Plan Your Mountain Elopement','de':'So plant ihr euer Berg-Elopement','es':'Cómo planear vuestro elopement de montaña'},
  'excerpt':{'en':'A simple, stress-free roadmap from first idea to \'I do\'.','de':'Ein einfacher, stressfreier Fahrplan von der Idee bis zum Ja-Wort.','es':'Una hoja de ruta simple y sin estrés, de la idea al \'sí, quiero\'.'},
  'intro':{'en':'Planning an elopement is far simpler than a big wedding — but a few decisions early on make everything flow. Here is the short version.',
           'de':'Ein Elopement zu planen ist viel einfacher als eine große Hochzeit — ein paar frühe Entscheidungen lassen alles fließen. Hier die Kurzfassung.',
           'es':'Planear un elopement es mucho más simple que una gran boda — pero unas pocas decisiones tempranas lo hacen todo fluir. Aquí la versión corta.'},
  'sec':[
   {'h':{'en':'1 · Choose the feeling, then the place','de':'1 · Erst das Gefühl, dann der Ort','es':'1 · Primero la sensación, luego el lugar'},
    'p':{'en':'Do you want adventure and effort, or calm and ease? That answer points us to the right region and location.',
         'de':'Wollt ihr Abenteuer und Anstrengung oder Ruhe und Leichtigkeit? Diese Antwort führt uns zur richtigen Region und zum Ort.',
         'es':'¿Queréis aventura y esfuerzo, o calma y sencillez? Esa respuesta nos lleva a la región y el lugar adecuados.'}},
   {'h':{'en':'2 · Pick a season and a date range','de':'2 · Saison und Zeitraum wählen','es':'2 · Elegid temporada y fechas'},
    'p':{'en':'We build in a weather buffer so we can move your day by a few hours or a day for the best conditions.',
         'de':'Wir planen einen Wetterpuffer ein, damit wir euren Tag um Stunden oder einen Tag verschieben können.',
         'es':'Añadimos un margen para el clima, para poder mover vuestro día unas horas o un día según las condiciones.'}},
   {'h':{'en':'3 · Leave the rest to us','de':'3 · Den Rest übernehmen wir','es':'3 · Dejadnos el resto'},
    'p':{'en':'Permits, timeline, flowers, hair & make-up, transfers and the legal path — all handled with our partners.',
         'de':'Genehmigungen, Ablauf, Blumen, Hair & Make-up, Transfers und das Rechtliche — alles mit unseren Partnern erledigt.',
         'es':'Permisos, cronograma, flores, peluquería y maquillaje, traslados y la parte legal — todo gestionado con nuestros socios.'}},
   {'h':{'en':'Permits, access &amp; the small costs','de':'Genehmigungen, Zugang &amp; die kleinen Kosten','es':'Permisos, acceso y los pequeños costes'},
    'p':{'en':'Beyond the big line items, a mountain day has small, easy-to-miss costs. Some locations need a photography or ceremony permit; the Tre Cime di Lavaredo toll road runs about &euro;30&ndash;45 per car; Lago di Braies has a summer access window and paid parking; cable-car tickets and a night in a rifugio add up too. None of it is expensive &mdash; it just needs planning, which we do for you. The ones nobody warns you about are in [[g:elopement-things-nobody-tells-you|what nobody tells you about eloping]].',
         'de':'Neben den großen Posten hat ein Bergtag kleine, leicht übersehene Kosten. Manche Orte brauchen eine Foto- oder Zeremonie-Genehmigung; die Mautstraße zu den Drei Zinnen kostet rund 30&ndash;45&nbsp;&euro; pro Auto; der Pragser Wildsee hat ein Sommer-Zufahrtsfenster und kostenpflichtige Parkplätze; auch Bergbahn-Tickets und eine Hüttennacht summieren sich. Teuer ist nichts davon &mdash; es braucht nur Planung, die wir übernehmen. Die Punkte, vor denen euch niemand warnt, stehen in [[g:elopement-things-nobody-tells-you|Was dir niemand über ein Elopement sagt]].',
         'es':'Más allá de las grandes partidas, un día en la montaña tiene pequeños costes fáciles de olvidar. Algunos lugares exigen permiso de fotografía o ceremonia; la carretera de peaje de las Tre Cime cuesta unos 30&ndash;45&nbsp;&euro; por coche; el Lago di Braies tiene una ventana de acceso estival y parking de pago; los billetes de teleférico y una noche en un refugio también suman. Nada de esto es caro &mdash; solo necesita planificación, que hacemos por vosotros. Los que nadie advierte están en [[g:elopement-things-nobody-tells-you|lo que nadie te cuenta sobre fugarse]].'}},
   {'h':{'en':'A day that never feels rushed','de':'Ein Tag, der sich nie gehetzt anfühlt','es':'Un día que nunca va con prisa'},
    'p':{'en':'A typical sunrise day starts in the dark: hair and make-up, a short drive or lift, then vows as the first light hits the rock. Portraits follow while the trails are still empty, then a long breakfast at a hut and time simply to be married. We build in a buffer &mdash; often a spare day &mdash; so weather never forces a rushed timeline. Deciding between first and last light? Read [[g:sunrise-or-sunset-elopement|sunrise or sunset?]], or see a full unhurried day in [[s:ultimate-italian-elopement|this three-day Italian elopement]].',
         'de':'Ein typischer Sonnenaufgangstag beginnt im Dunkeln: Hair &amp; Make-up, eine kurze Fahrt oder Bergbahn, dann das Ja, wenn das erste Licht den Fels trifft. Danach Porträts, solange die Wege leer sind, ein langes Frühstück auf der Hütte und einfach Zeit, verheiratet zu sein. Wir planen einen Puffer ein &mdash; oft einen Reservetag &mdash; damit das Wetter nie zur Hetze zwingt. Unentschieden zwischen erstem und letztem Licht? Lest [[g:sunrise-or-sunset-elopement|Sonnenaufgang oder Sonnenuntergang?]], oder seht einen ganzen entspannten Tag in [[s:ultimate-italian-elopement|diesem dreitägigen italienischen Elopement]].',
         'es':'Un día de amanecer típico empieza a oscuras: peluquería y maquillaje, un trayecto corto o un remonte, y los votos cuando la primera luz toca la roca. Siguen los retratos con los senderos aún vacíos, un desayuno largo en un refugio y tiempo simplemente para estar casados. Añadimos un margen &mdash; a menudo un día extra &mdash; para que el clima nunca imponga prisas. ¿Dudáis entre la primera y la última luz? Leed [[g:sunrise-or-sunset-elopement|¿amanecer o atardecer?]], o ved un día entero sin prisa en [[s:ultimate-italian-elopement|este elopement italiano de tres días]].'}},
  ]},
 {'slug':'most-beautiful-dolomites-spots','img':'s19',
  'title':{'en':'The Most Beautiful Places in the Dolomites','de':'Die schönsten Orte in den Dolomiten','es':'Los lugares más bellos de los Dolomitas'},
  'excerpt':{'en':'Our favourite peaks, lakes and ridges for an unforgettable elopement.','de':'Unsere liebsten Gipfel, Seen und Grate für ein unvergessliches Elopement.','es':'Nuestras cumbres, lagos y crestas favoritos para un elopement inolvidable.'},
  'intro':{'en':'After years of shooting here, a handful of places keep drawing us back — each with its own light, mood and effort. Here are the ones we love most, and how to choose between them.','de':'Nach Jahren hier ziehen uns einige wenige Orte immer wieder an — jeder mit eigenem Licht, eigener Stimmung und eigenem Aufwand. Das sind unsere liebsten und wie ihr euch entscheidet.','es':'Tras años fotografiando aquí, unos pocos lugares nos siguen atrayendo — cada uno con su luz, su ambiente y su esfuerzo. Estos son nuestros favoritos y cómo elegir.'},
  'sec':[
   {'h':{'en':'Lago di Braies &amp; the great lakes','de':'Pragser Wildsee &amp; die großen Seen','es':'Lago di Braies y los grandes lagos'},
    'p':{'en':'Emerald water, the old boathouse and peaks rising straight from the shore. Braies is iconic &mdash; and at dawn, before the boats, wonderfully quiet.','de':'Smaragdgrünes Wasser, das alte Bootshaus und Gipfel, die direkt aus dem Ufer wachsen. Braies ist ikonisch &mdash; und im Morgengrauen, vor den Booten, herrlich still.','es':'Agua esmeralda, la vieja caseta y cumbres que surgen de la orilla. Braies es icónico &mdash; y al alba, antes de las barcas, maravillosamente tranquilo.'}},
   {'h':{'en':'Seceda, Tre Cime &amp; the high ridges','de':'Seceda, Drei Zinnen &amp; die hohen Grate','es':'Seceda, Tre Cime y las crestas altas'},
    'p':{'en':'For sheer drama, nothing beats the jagged ridgelines. Some are a short cable-car ride away, others a proper hike &mdash; we match the spot to how far you want to walk.','de':'Für pure Dramatik geht nichts über die zackigen Grate. Manche sind nur eine kurze Seilbahnfahrt entfernt, andere eine echte Wanderung &mdash; wir wählen den Ort nach eurer Gehstrecke.','es':'Para puro drama, nada supera las crestas dentadas. Algunas están a un corto teleférico; otras, a una buena caminata &mdash; elegimos según cuánto queráis andar.'}},
   {'h':{'en':'Hidden lakes for the adventurous','de':'Versteckte Seen für Abenteuerlustige','es':'Lagos escondidos para los aventureros'},
    'p':{'en':'Away from the icons, quieter water rewards a walk. Lago di Sorapis glows an unreal milky turquoise a couple of hours from Passo Tre Croci; Lago di Federa mirrors the Croda da Lago inside a ring of larches; little Lago di Limides catches the Tofane just off Passo Falzarego; and roadside Lago d\'Antorno frames the Cadini spires with no effort at all. These are the spots we send couples who want Braies\' beauty without Braies\' crowds &mdash; and they photograph beautifully in any weather, as [[s:pizza-elopement-at-tre-cime-cadini-di-misurina|this day near the Tre Cime]] shows.',
         'de':'Abseits der Ikonen belohnt stilleres Wasser einen Fußweg. Der Lago di Sorapis leuchtet in unwirklichem milchigem Türkis, zwei Stunden vom Passo Tre Croci; der Lago di Federa spiegelt die Croda da Lago in einem Kranz aus Lärchen; der kleine Lago di Limides fängt die Tofane direkt am Falzaregopass ein; und der Lago d\'Antorno am Straßenrand rahmt die Cadini-Zinnen ganz ohne Aufwand. Das sind die Orte für Paare, die Braies\' Schönheit ohne Braies\' Trubel wollen &mdash; und sie fotografieren sich bei jedem Wetter schön, wie [[s:pizza-elopement-at-tre-cime-cadini-di-misurina|dieser Tag bei den Drei Zinnen]] zeigt.',
         'es':'Lejos de los iconos, el agua más tranquila premia una caminata. El Lago di Sorapis brilla en un turquesa lechoso irreal a un par de horas del Passo Tre Croci; el Lago di Federa refleja la Croda da Lago en un anillo de alerces; el pequeño Lago di Limides recoge las Tofane junto al Passo Falzarego; y el Lago d\'Antorno, junto a la carretera, enmarca las agujas de los Cadini sin esfuerzo. Son los lugares para parejas que quieren la belleza de Braies sin su gentío &mdash; y se fotografían preciosos con cualquier tiempo, como muestra [[s:pizza-elopement-at-tre-cime-cadini-di-misurina|este día junto a las Tre Cime]].'}},
   {'h':{'en':'Passes, meadows &amp; the Cinque Torri','de':'Pässe, Wiesen &amp; die Cinque Torri','es':'Puertos, prados y las Cinque Torri'},
    'p':{'en':'For big scenery you can almost drive to, the high passes are hard to beat. Passo Giau is a meadow amphitheatre ringed by peaks; Cinque Torri &mdash; five tower-like rocks reached by a short chairlift from Bai de Dones &mdash; give an intimate stage with a First-World-War history; and the Averau and Nuvolau refuges above them serve dinner with a 360&deg; view. These roadside and lift-served spots are perfect when you\'d rather save your legs for dancing &mdash; and glorious for [[g:sunrise-or-sunset-elopement|both sunrise and sunset]].',
         'de':'Für große Kulisse, zu der man fast hinfahren kann, sind die Hochpässe kaum zu schlagen. Der Passo Giau ist ein Wiesen-Amphitheater im Kranz der Gipfel; die Cinque Torri &mdash; fünf turmartige Felsen, erreichbar mit einem kurzen Sessellift ab Bai de Dones &mdash; sind eine intime Bühne mit Geschichte aus dem Ersten Weltkrieg; und die Hütten Averau und Nuvolau darüber servieren Abendessen mit 360&deg;-Blick. Diese Orte am Straßenrand oder per Lift sind ideal, wenn ihr die Beine lieber fürs Tanzen schont &mdash; und herrlich bei [[g:sunrise-or-sunset-elopement|Sonnenauf- wie Sonnenuntergang]].',
         'es':'Para gran paisaje al que casi se llega en coche, los puertos altos son difíciles de superar. El Passo Giau es un anfiteatro de prados rodeado de cumbres; las Cinque Torri &mdash; cinco rocas como torres, con un corto telesilla desde Bai de Dones &mdash; ofrecen un escenario íntimo con historia de la Primera Guerra Mundial; y los refugios Averau y Nuvolau sobre ellas sirven cena con vistas de 360&deg;. Estos lugares junto a la carretera o con remonte son ideales si preferís guardar las piernas para bailar &mdash; y gloriosos [[g:sunrise-or-sunset-elopement|tanto al amanecer como al atardecer]].'}},
   {'h':{'en':'How to reach each one','de':'Wie ihr jeden erreicht','es':'Cómo llegar a cada uno'},
    'p':{'en':'Access decides your morning. Braies limits summer traffic to the lake from roughly 10:00 to 16:00, so we go before it; the Tre Cime toll road (about &euro;30&ndash;45 per car) drives you almost to the base; Seceda, Lagazuoi and Faloria are cable cars; Sorapis and Federa are hikes with no vehicle access. We plan the route, the tickets and the timing around all of it &mdash; the full logistics live in [[g:how-to-plan-your-elopement|how to plan your elopement]].',
         'de':'Der Zugang entscheidet über euren Morgen. Braies begrenzt den Sommerverkehr zum See etwa von 10 bis 16 Uhr, also fahren wir davor; die Mautstraße zu den Drei Zinnen (rund 30&ndash;45&nbsp;&euro; pro Auto) bringt euch fast bis unter die Zinnen; Seceda, Lagazuoi und Faloria sind Seilbahnen; Sorapis und Federa sind Wanderungen ohne Autozufahrt. Wir planen Route, Tickets und Timing rundherum &mdash; die ganze Logistik steht in [[g:how-to-plan-your-elopement|So plant ihr euer Berg-Elopement]].',
         'es':'El acceso decide vuestra mañana. Braies limita el tráfico estival al lago de 10:00 a 16:00, así que vamos antes; la carretera de peaje de las Tre Cime (unos 30&ndash;45&nbsp;&euro; por coche) os deja casi en la base; Seceda, Lagazuoi y Faloria son teleféricos; Sorapis y Federa son caminatas sin acceso en coche. Planeamos la ruta, los billetes y los tiempos alrededor de todo ello &mdash; la logística completa está en [[g:how-to-plan-your-elopement|cómo planear vuestro elopement]].'}},
  ]},
 {'slug':'helicopter-elopement-dolomites-guide','img':'s11',
  'title':{'en':'The Helicopter Elopement Guide','de':'Der Helikopter-Elopement-Guide','es':'La guía del elopement en helicóptero'},
  'excerpt':{'en':'How to marry on a summit almost no one can reach — by air.','de':'Wie ihr auf einem Gipfel heiratet, den fast niemand erreicht — aus der Luft.','es':'Cómo casaros en una cumbre casi inaccesible — por aire.'},
  'intro':{'en':'A helicopter turns a multi-day trek into minutes and lands you where the crowds never follow. Here is how a heli elopement actually works, what it costs and what to expect.','de':'Ein Helikopter macht aus einer Mehrtagestour Minuten und setzt euch dort ab, wohin keine Menschenmenge folgt. So läuft ein Heli-Elopement wirklich ab &mdash; Kosten und Ablauf.','es':'Un helicóptero convierte una travesía de días en minutos y os deja donde la multitud no llega. Así funciona de verdad un elopement en helicóptero &mdash; coste y desarrollo.'},
  'sec':[
   {'h':{'en':'How the day flows','de':'Wie der Tag abläuft','es':'Cómo transcurre el día'},
    'p':{'en':'You fly from a valley helipad to a remote ledge or glacier, exchange vows with the whole range beneath you, and fly back &mdash; often with time for a second location. The flight itself becomes part of the story.','de':'Ihr fliegt von einem Talhubschrauberplatz zu einem einsamen Felsband oder Gletscher, gebt euch das Ja mit dem ganzen Massiv zu Füßen und fliegt zurück &mdash; oft bleibt Zeit für einen zweiten Ort. Der Flug selbst wird Teil der Geschichte.','es':'Voláis desde un helipuerto del valle a un rincón remoto o un glaciar, os dais el sí con toda la cordillera a los pies y regresáis &mdash; a menudo con tiempo para un segundo lugar. El vuelo se vuelve parte de la historia.'}},
   {'h':{'en':'Cost &amp; planning','de':'Kosten &amp; Planung','es':'Coste y planificación'},
    'p':{'en':'Expect roughly &euro;2,500 upward for the flight, depending on the landing site and time of day. Weather decides everything, so we always hold a flexible window &mdash; and a beautiful ground plan B.','de':'Rechnet grob ab &euro;2.500 für den Flug, je nach Landeplatz und Tageszeit. Das Wetter entscheidet alles, deshalb halten wir immer ein flexibles Fenster &mdash; und einen schönen Boden-Plan-B.','es':'Contad desde unos &euro;2.500 para el vuelo, según el lugar de aterrizaje y la hora. El tiempo lo decide todo, por eso mantenemos una ventana flexible &mdash; y un bonito plan B en tierra.'}},
   {'h':{'en':'Where a helicopter can take you','de':'Wohin ein Helikopter euch bringt','es':'Adónde os puede llevar un helicóptero'},
    'p':{'en':'A flight opens ground that a normal elopement never reaches: a remote rock ledge, a glacier plateau on the Marmolada, a summit that would otherwise be a two-day climb. Landings are flown by licensed alpine operators to approved sites, usually a short set-down for the ceremony and portraits before the flight home. The flight itself becomes half the story &mdash; see it in [[s:adventure-helicopter-elopement-dolomites|our helicopter elopement]].',
         'de':'Ein Flug öffnet Gelände, das ein normales Elopement nie erreicht: ein einsames Felsband, ein Gletscherplateau auf der Marmolada, ein Gipfel, der sonst eine Zwei-Tage-Tour wäre. Landungen fliegen lizenzierte Alpin-Betreiber zu genehmigten Plätzen &mdash; meist ein kurzes Absetzen für Zeremonie und Porträts vor dem Rückflug. Der Flug selbst wird zur halben Geschichte &mdash; zu sehen in [[s:adventure-helicopter-elopement-dolomites|unserem Helikopter-Elopement]].',
         'es':'Un vuelo abre terreno que un elopement normal nunca alcanza: un saliente de roca remoto, una meseta glaciar en la Marmolada, una cumbre que si no sería una ascensión de dos días. Los aterrizajes los vuelan operadores alpinos autorizados a lugares aprobados, normalmente una breve parada para la ceremonia y los retratos antes del regreso. El vuelo en sí se vuelve media historia &mdash; vedlo en [[s:adventure-helicopter-elopement-dolomites|nuestro elopement en helicóptero]].'}},
   {'h':{'en':'Helicopter, cable car or hike?','de':'Helikopter, Bergbahn oder Wanderung?','es':'¿Helicóptero, teleférico o caminata?'},
    'p':{'en':'The flight is the boldest way up, but not the only one. If you want the summit feeling without the price, a cable car to Lagazuoi, Sass Pordoi or Seceda delivers an enormous view for the cost of a ticket; if you want the day to feel earned, a hike gives you solitude and costs nothing. We often combine them &mdash; fly in, walk to a quieter ledge. Weigh the view against the effort in [[g:most-beautiful-dolomites-spots|the most beautiful spots]], and the budget in [[g:how-to-plan-your-elopement|how to plan]].',
         'de':'Der Flug ist der kühnste Weg nach oben, aber nicht der einzige. Wollt ihr das Gipfelgefühl ohne den Preis, liefert eine Bergbahn zum Lagazuoi, Sass Pordoi oder Seceda einen gewaltigen Blick zum Ticketpreis; soll sich der Tag verdient anfühlen, schenkt eine Wanderung Einsamkeit und kostet nichts. Oft kombinieren wir beides &mdash; einfliegen, zu einem stilleren Band gehen. Wägt Aussicht gegen Aufwand in [[g:most-beautiful-dolomites-spots|den schönsten Orten]] und das Budget in [[g:how-to-plan-your-elopement|So plant ihr]].',
         'es':'El vuelo es la forma más audaz de subir, pero no la única. Si queréis la sensación de cumbre sin el precio, un teleférico al Lagazuoi, Sass Pordoi o Seceda da una vista enorme por el coste de un billete; si queréis que el día se sienta ganado, una caminata os da soledad y no cuesta nada. A menudo los combinamos &mdash; volar y caminar a un saliente más tranquilo. Sopesad vista y esfuerzo en [[g:most-beautiful-dolomites-spots|los lugares más bellos]], y el presupuesto en [[g:how-to-plan-your-elopement|cómo planear]].'}},
  ]},
 {'slug':'mountain-proposal-guide','img':'s20',
  'title':{'en':'How to Plan a Mountain Proposal','de':'Einen Antrag in den Bergen planen','es':'Cómo planear una pedida en la montaña'},
  'excerpt':{'en':'Pull off the surprise — and have it captured as it happens.','de':'Die Überraschung gelingt — und wird festgehalten, während sie passiert.','es':'Que la sorpresa salga bien — y quede capturada mientras ocurre.'},
  'intro':{'en':'A proposal in the mountains is equal parts logistics and nerve. Here is how we help you choose the moment, keep it a secret, and photograph it without your partner ever noticing us.','de':'Ein Antrag in den Bergen ist Logistik und Nerven zugleich. So helfen wir euch, den Moment zu wählen, ihn geheim zu halten und ihn zu fotografieren, ohne dass euer Gegenüber uns bemerkt.','es':'Una pedida en la montaña es logística y nervios a partes iguales. Así os ayudamos a elegir el momento, mantener el secreto y fotografiarlo sin que vuestra pareja nos vea.'},
  'sec':[
   {'h':{'en':'Choosing the moment','de':'Den Moment wählen','es':'Elegir el momento'},
    'p':{'en':'First light is our favourite: quiet trails, soft colour and almost no one around. We scout a spot with a natural pause &mdash; a summit, a viewpoint, a lakeshore &mdash; where kneeling feels effortless.','de':'Das erste Licht ist unser Favorit: stille Wege, weiche Farben, kaum jemand da. Wir suchen einen Ort mit natürlicher Pause &mdash; Gipfel, Aussichtspunkt, Seeufer &mdash; wo das Niederknien mühelos wirkt.','es':'La primera luz es nuestra favorita: senderos tranquilos, color suave y casi nadie. Buscamos un lugar con una pausa natural &mdash; cumbre, mirador, orilla &mdash; donde arrodillarse resulte natural.'}},
   {'h':{'en':'Keeping it a secret','de':'Das Geheimnis wahren','es':'Guardar el secreto'},
    'p':{'en':'We plan everything by message, shoot from a distance with a long lens, and pass for ordinary hikers until the yes. Afterwards we stay for a proper couples session to celebrate.','de':'Wir planen alles per Nachricht, fotografieren aus der Distanz mit Teleobjektiv und geben uns bis zum Ja als gewöhnliche Wanderer aus. Danach bleiben wir für ein richtiges Paar-Shooting zum Feiern.','es':'Lo planeamos todo por mensaje, fotografiamos de lejos con teleobjetivo y pasamos por senderistas normales hasta el sí. Después nos quedamos para una sesión de pareja y celebrarlo.'}},
   {'h':{'en':'Spots that make the surprise easy','de':'Orte, die die Überraschung leicht machen','es':'Lugares que hacen fácil la sorpresa'},
    'p':{'en':'The best proposal spots need a natural reason to pause and little effort &mdash; a long sweaty hike tends to give the game away. Cable-car viewpoints are ideal: the Seceda ridge, Sass Pordoi\'s terrace, or the Nordkette minutes above Innsbruck. So are roadside lakes like Lago di Braies\' boardwalk or little Lago d\'Antorno. Go at first light and you\'ll have the railing to yourselves. Pick from [[g:best-alps-elopement-locations|our best Alpine locations]].',
         'de':'Die besten Antragsorte brauchen einen natürlichen Grund für eine Pause und wenig Aufwand &mdash; eine lange, schweißtreibende Wanderung verrät oft alles. Bergbahn-Aussichten sind ideal: der Seceda-Grat, die Terrasse des Sass Pordoi oder die Nordkette wenige Minuten über Innsbruck. Ebenso Seen am Straßenrand wie der Steg am Pragser Wildsee oder der kleine Lago d\'Antorno. Kommt bei erstem Licht, dann gehört das Geländer euch allein. Wählt aus [[g:best-alps-elopement-locations|unseren besten Alpen-Orten]].',
         'es':'Los mejores lugares para la pedida necesitan un motivo natural para parar y poco esfuerzo &mdash; una caminata larga y sudorosa suele delatar el plan. Los miradores de teleférico son ideales: la cresta del Seceda, la terraza del Sass Pordoi o la Nordkette a minutos de Innsbruck. También lagos junto a la carretera como la pasarela del Lago di Braies o el pequeño Lago d\'Antorno. Id con la primera luz y tendréis la baranda para vosotros. Elegid entre [[g:best-alps-elopement-locations|nuestros mejores lugares alpinos]].'}},
   {'h':{'en':'The ring, the weather &amp; a plan B','de':'Der Ring, das Wetter &amp; ein Plan B','es':'El anillo, el clima y un plan B'},
    'p':{'en':'Keep the ring in a zipped, secure pocket on the walk &mdash; not a coat you might hand over. First light gives you empty trails and soft colour, but mountain weather turns fast, so we always hold a backup spot and a spare morning. After the yes we keep shooting for a relaxed couples session and can turn a few images around the same day. Then celebrate properly &mdash; a real morning-after glow is [[s:mountain-engagement|this mountain engagement]].',
         'de':'Tragt den Ring auf dem Weg in einer geschlossenen, sicheren Tasche &mdash; nicht in einer Jacke, die ihr weggebt. Das erste Licht schenkt leere Wege und weiche Farben, doch Bergwetter kippt schnell, deshalb halten wir immer einen Ausweichort und einen Reservemorgen bereit. Nach dem Ja fotografieren wir weiter für ein entspanntes Paar-Shooting und liefern noch am selben Tag ein paar Bilder. Danach wird gefeiert &mdash; ein echtes Nachglühen ist [[s:mountain-engagement|diese Verlobung in den Bergen]].',
         'es':'Llevad el anillo en un bolsillo cerrado y seguro durante la caminata &mdash; no en un abrigo que podríais entregar. La primera luz da senderos vacíos y color suave, pero el tiempo de montaña cambia rápido, por eso siempre reservamos un lugar alternativo y una mañana de repuesto. Tras el sí seguimos fotografiando para una sesión de pareja relajada y podemos entregar unas imágenes el mismo día. Luego, a celebrar &mdash; un verdadero brillo del día después es [[s:mountain-engagement|este compromiso en la montaña]].'}},
  ]},
 {'slug':'sunrise-or-sunset-elopement','img':'s21',
  'title':{'en':'Sunrise or Sunset for Your Elopement?','de':'Sonnenaufgang oder Sonnenuntergang?','es':'¿Amanecer o atardecer para vuestro elopement?'},
  'excerpt':{'en':'Two very different days — here is how to choose your light.','de':'Zwei ganz verschiedene Tage — so wählt ihr euer Licht.','es':'Dos días muy distintos — así elegís vuestra luz.'},
  'intro':{'en':'The same summit feels like two different places at dawn and at dusk. The choice shapes your whole day &mdash; the effort, the crowds and the mood. Here is how we help you decide.','de':'Derselbe Gipfel wirkt bei Morgen- und Abendlicht wie zwei verschiedene Orte. Die Wahl prägt euren ganzen Tag &mdash; Aufwand, Trubel und Stimmung. So helfen wir euch bei der Entscheidung.','es':'La misma cumbre parece dos lugares distintos al alba y al ocaso. La elección marca todo el día &mdash; el esfuerzo, la gente y el ambiente. Así os ayudamos a decidir.'},
  'sec':[
   {'h':{'en':'Sunrise: solitude &amp; soft light','de':'Sonnenaufgang: Ruhe &amp; weiches Licht','es':'Amanecer: soledad y luz suave'},
    'p':{'en':'A pre-dawn start buys you empty trails and the pink alpenglow before the valley wakes. It asks for an early alarm and warm layers &mdash; but the stillness is unmatched.','de':'Ein Start vor Morgengrauen schenkt euch leere Wege und das rosa Alpenglühen, ehe das Tal erwacht. Es verlangt frühes Aufstehen und warme Schichten &mdash; doch die Stille ist unübertroffen.','es':'Salir antes del alba os da senderos vacíos y el alpenglow rosado antes de que despierte el valle. Pide madrugar y capas de abrigo &mdash; pero la quietud no tiene igual.'}},
   {'h':{'en':'Sunset: warm &amp; unhurried','de':'Sonnenuntergang: warm &amp; gemächlich','es':'Atardecer: cálido y sin prisa'},
    'p':{'en':'Golden hour is easier &mdash; no alarm, a slow walk up, and warm light that lingers. The trade-off is more people, so we pick lesser-known spots to keep it intimate.','de':'Die goldene Stunde ist bequemer &mdash; kein Wecker, ein gemächlicher Aufstieg, warmes Licht, das bleibt. Der Preis: mehr Menschen, deshalb wählen wir weniger bekannte Orte.','es':'La hora dorada es más fácil &mdash; sin despertador, subida tranquila y luz cálida que perdura. A cambio hay más gente, así que elegimos rincones menos conocidos.'}},
   {'h':{'en':'Best spots for sunrise','de':'Beste Orte für den Sonnenaufgang','es':'Mejores lugares para el amanecer'},
    'p':{'en':'Dawn suits places you can reach before the lifts run. Lago di Braies is magic before its 10:00 traffic window, mirror-still and empty; the Tre Cime toll road is open through the night, so you can drive up for first light on the peaks; and ridges like Seceda mean either a head-torch hike or a night in a rifugio, because the first cabin comes up too late for the colour. See a real daybreak in [[s:sunrise-dolomites-elopement|this sunrise elopement]].',
         'de':'Der Morgen passt zu Orten, die ihr vor den Bahnen erreicht. Der Pragser Wildsee ist vor seinem 10-Uhr-Verkehrsfenster magisch &mdash; spiegelglatt und leer; die Mautstraße zu den Drei Zinnen ist nachts geöffnet, ihr könnt also zum ersten Licht hinauffahren; und Grate wie die Seceda bedeuten entweder einen Stirnlampen-Aufstieg oder eine Hüttennacht, weil die erste Gondel zu spät für die Farbe kommt. Ein echter Tagesanbruch ist [[s:sunrise-dolomites-elopement|dieses Sonnenaufgangs-Elopement]].',
         'es':'El alba va con lugares a los que llegáis antes de que funcionen los remontes. El Lago di Braies es mágico antes de su ventana de tráfico de las 10:00 &mdash; espejado y vacío; la carretera de peaje de las Tre Cime abre de noche, así que podéis subir para la primera luz en las cumbres; y crestas como el Seceda implican o una subida con frontal o una noche en un refugio, porque la primera cabina llega tarde para el color. Ved un amanecer real en [[s:sunrise-dolomites-elopement|este elopement al amanecer]].'}},
   {'h':{'en':'Best spots for sunset','de':'Beste Orte für den Sonnenuntergang','es':'Mejores lugares para el atardecer'},
    'p':{'en':'Evening favours cable-car viewpoints where you can catch the last cabin down &mdash; or, better, sleep at the top. The Sass Pordoi terrace, Lagazuoi with its clifftop refuge, the Alpe di Siusi meadows and the Nordkette above Innsbruck all glow at golden hour and stay quiet once the day-trippers leave. Always check the last descent time; where there isn\'t one, we book the rifugio. More in [[g:most-beautiful-dolomites-spots|the most beautiful spots]], and a warm Tyrolean evening in [[s:sunset-elopement-tyrol|this sunset elopement]].',
         'de':'Der Abend begünstigt Bergbahn-Aussichten, wo ihr die letzte Gondel nach unten erwischt &mdash; oder besser oben schlaft. Die Sass-Pordoi-Terrasse, der Lagazuoi mit seiner Hütte am Abgrund, die Wiesen der Seiser Alm und die Nordkette über Innsbruck glühen zur goldenen Stunde und bleiben still, sobald die Tagesgäste weg sind. Prüft immer die letzte Talfahrt; wo es keine gibt, buchen wir die Hütte. Mehr in [[g:most-beautiful-dolomites-spots|den schönsten Orten]], und ein warmer Tiroler Abend in [[s:sunset-elopement-tyrol|dieser Sonnenuntergangs-Hochzeit]].',
         'es':'La tarde favorece los miradores de teleférico donde podéis coger la última cabina de bajada &mdash; o, mejor, dormir arriba. La terraza del Sass Pordoi, el Lagazuoi con su refugio al borde del precipicio, los prados del Alpe di Siusi y la Nordkette sobre Innsbruck brillan en la hora dorada y quedan tranquilos cuando se van los excursionistas de día. Comprobad siempre la hora de la última bajada; donde no la hay, reservamos el refugio. Más en [[g:most-beautiful-dolomites-spots|los lugares más bellos]], y una cálida tarde tirolesa en [[s:sunset-elopement-tyrol|este elopement al atardecer]].'}},
  ]},
 {'slug':'elopement-things-nobody-tells-you','img':'s22',
  'title':{'en':'What Nobody Tells You About Eloping','de':'Was dir niemand über ein Elopement sagt','es':'Lo que nadie te cuenta sobre fugarse'},
  'excerpt':{'en':'The small things that make or break the day — don\'t forget these.','de':'Die kleinen Dinge, die den Tag ausmachen — vergesst diese nicht.','es':'Los pequeños detalles que lo cambian todo — no os olvidéis de estos.'},
  'intro':{'en':'The big decisions are the easy part. It\'s the small, unglamorous details that quietly make a mountain day perfect &mdash; the ones no checklist mentions. Here are the ones we learned the hard way.','de':'Die großen Entscheidungen sind der leichte Teil. Es sind die kleinen, unspektakulären Details, die einen Bergtag leise perfekt machen &mdash; die, die keine Checkliste nennt. Hier die, die wir schmerzhaft gelernt haben.','es':'Las grandes decisiones son lo fácil. Son los pequeños detalles sin glamur los que hacen perfecto un día en la montaña &mdash; los que ninguna lista menciona. Estos los aprendimos a las malas.'},
  'sec':[
   {'h':{'en':'Comfort beats everything','de':'Komfort schlägt alles','es':'La comodidad gana a todo'},
    'p':{'en':'Pack a second pair of shoes for the walk, hand warmers, water and a snack. Cold, blistered or hungry always shows in the photos &mdash; and in how the day feels.','de':'Nehmt Wechselschuhe für den Weg, Handwärmer, Wasser und einen Snack mit. Kalt, mit Blasen oder hungrig sieht man immer auf den Fotos &mdash; und spürt es im Tag.','es':'Llevad un segundo par de zapatos para caminar, calentadores de manos, agua y algo de comer. El frío, las ampollas o el hambre siempre se ven en las fotos &mdash; y en cómo se siente el día.'}},
   {'h':{'en':'Protect the moment','de':'Den Moment schützen','es':'Proteger el momento'},
    'p':{'en':'Write your vows in advance and bring a printed copy &mdash; screens die in the cold. Tell no one the exact spot, silence your phones, and leave buffer time so nothing feels rushed.','de':'Schreibt euer Ehegelübde vorab und bringt einen Ausdruck mit &mdash; Displays sterben in der Kälte. Verratet den genauen Ort niemandem, stellt die Handys stumm und plant Puffer, damit nichts hetzt.','es':'Escribid los votos con antelación y llevad una copia impresa &mdash; las pantallas mueren con el frío. No digáis el lugar exacto, silenciad los móviles y dejad margen para que nada vaya con prisa.'}},
   {'h':{'en':'The practical things nobody mentions','de':'Die praktischen Dinge, die niemand erwähnt','es':'Lo práctico que nadie menciona'},
    'p':{'en':'Carry a little cash: some toll roads and car parks &mdash; the Tre Cime road, Braies parking &mdash; are smoother paid in cash, and mountain-hut kitchens sometimes are too. Check the last cable-car descent before you commit to sunset, remember Braies closes to traffic from about 10:00 in summer, and pack a warm layer even in August &mdash; a summit at dawn is cold. And don\'t fear a grey forecast: rain can be the best thing that happens, as [[s:rainy-lago-di-braies-pizza-elopement|this rainy Braies morning]] shows.',
         'de':'Habt etwas Bargeld dabei: Manche Mautstraßen und Parkplätze &mdash; die Drei-Zinnen-Straße, der Parkplatz am Pragser Wildsee &mdash; gehen bar reibungsloser, und Hüttenküchen manchmal auch. Prüft die letzte Talfahrt der Bergbahn, bevor ihr euch auf den Sonnenuntergang festlegt, denkt daran, dass Braies im Sommer ab etwa 10 Uhr für den Verkehr sperrt, und packt selbst im August eine warme Schicht ein &mdash; ein Gipfel im Morgengrauen ist kalt. Und fürchtet keine graue Vorhersage: Regen kann das Beste sein, das passiert, wie [[s:rainy-lago-di-braies-pizza-elopement|dieser Regenmorgen am Pragser Wildsee]] zeigt.',
         'es':'Llevad algo de efectivo: algunas carreteras de peaje y aparcamientos &mdash; la carretera de las Tre Cime, el parking de Braies &mdash; van más fluidos en efectivo, y a veces también las cocinas de los refugios. Comprobad la última bajada del teleférico antes de comprometeros con el atardecer, recordad que Braies cierra al tráfico desde las 10:00 en verano, y llevad una capa de abrigo incluso en agosto &mdash; una cumbre al alba es fría. Y no temáis un pronóstico gris: la lluvia puede ser lo mejor que pase, como muestra [[s:rainy-lago-di-braies-pizza-elopement|esta mañana lluviosa en Braies]].'}},
   {'h':{'en':'The small print that saves you money','de':'Das Kleingedruckte, das Geld spart','es':'La letra pequeña que ahorra dinero'},
    'p':{'en':'A few early decisions cut the cost. Book the rifugio and, if you\'re marrying legally in Austria, the registrar months ahead &mdash; both are limited in summer. The off-season (late May, October) is cheaper, quieter and often more beautiful, with golden larches and dusted peaks. And you rarely need both a toll road and a cable car on the same day &mdash; picking one keeps the budget and the timeline simple. We map all of it in [[g:how-to-plan-your-elopement|how to plan your elopement]].',
         'de':'Ein paar frühe Entscheidungen senken die Kosten. Bucht die Hütte und, wenn ihr in Österreich rechtsgültig heiratet, das Standesamt Monate im Voraus &mdash; beides ist im Sommer knapp. Die Nebensaison (spätes Mai, Oktober) ist günstiger, ruhiger und oft schöner, mit goldenen Lärchen und angezuckerten Gipfeln. Und ihr braucht selten Mautstraße und Bergbahn am selben Tag &mdash; eines zu wählen hält Budget und Ablauf einfach. Alles dazu in [[g:how-to-plan-your-elopement|So plant ihr euer Berg-Elopement]].',
         'es':'Unas pocas decisiones tempranas reducen el coste. Reservad el refugio y, si os casáis legalmente en Austria, el registro con meses de antelación &mdash; ambos son limitados en verano. La temporada baja (finales de mayo, octubre) es más barata, tranquila y a menudo más bella, con alerces dorados y cumbres nevadas. Y rara vez necesitáis carretera de peaje y teleférico el mismo día &mdash; elegir uno mantiene el presupuesto y el horario simples. Lo mapeamos todo en [[g:how-to-plan-your-elopement|cómo planear vuestro elopement]].'}},
  ]},
]

STORYBY={s[1]:s for s in STORIES}

# extra structure per guide: facts [(labelkey,{lang:value})], sec4 {h,p}, tips {lang:[..]}, related story slugs
GUIDE_EXTRA={
 'dolomites-elopement-guide':{
   'facts':[('season',{'en':'Jun&ndash;Sep','de':'Juni&ndash;Sep','es':'Jun&ndash;Sep'}),
            ('diff',{'en':'Easy&ndash;Challenging','de':'Leicht&ndash;Anspruchsvoll','es':'Fácil&ndash;Exigente'}),
            ('reach',{'en':'Venice / Innsbruck &middot; 2&ndash;3 h','de':'Venedig / Innsbruck &middot; 2&ndash;3 h','es':'Venecia / Innsbruck &middot; 2&ndash;3 h'})],
   'sec4':{'h':{'en':'Sunrise or sunset?','de':'Sonnenaufgang oder Sonnenuntergang?','es':'¿Amanecer o atardecer?'},
           'p':{'en':'Sunrise means solitude and soft light with a pre-dawn start; sunset is easier but busier. We help you choose what fits you.',
                'de':'Sonnenaufgang bedeutet Ruhe und weiches Licht mit frühem Start; Sonnenuntergang ist bequemer, aber belebter. Wir helfen euch bei der Wahl.',
                'es':'El amanecer trae soledad y luz suave con un inicio antes del alba; el atardecer es más cómodo pero con más gente. Os ayudamos a elegir.'}},
   'tips':{'en':['Book mountain huts early for sunrise access.','The larches glow most in late September.','Keep your date weather-flexible.'],
           'de':['Hütten früh buchen für den Zugang zum Sonnenaufgang.','Die Lärchen leuchten Ende September am schönsten.','Haltet euer Datum wetterflexibel.'],
           'es':['Reservad los refugios pronto para el amanecer.','Los alerces brillan más a finales de septiembre.','Mantened una fecha flexible según el clima.']},
   'stories':['climbing-wedding','sunrise-dolomites-elopement','lago-di-braies-elopement']},
 'elope-in-austria':{
   'facts':[('season',{'en':'May&ndash;Oct','de':'Mai&ndash;Okt','es':'May&ndash;Oct'}),
            ('diff',{'en':'Easy&ndash;Moderate','de':'Leicht&ndash;Mittel','es':'Fácil&ndash;Moderada'}),
            ('reach',{'en':'Innsbruck airport','de':'Flughafen Innsbruck','es':'Aeropuerto de Innsbruck'})],
   'sec4':{'h':{'en':'Symbolic or legal ceremony?','de':'Symbolisch oder standesamtlich?','es':'¿Ceremonia simbólica o legal?'},
           'p':{'en':'Marry officially at home and celebrate a symbolic ceremony on the mountain, or complete the legal marriage in Austria &mdash; both work beautifully.',
                'de':'Heiratet offiziell zu Hause und feiert eine symbolische Zeremonie am Berg &mdash; oder erledigt die Trauung rechtsgültig in Österreich. Beides funktioniert wunderbar.',
                'es':'Casaos oficialmente en casa y celebrad una ceremonia simbólica en la montaña, o completad la boda legal en Austria &mdash; ambas opciones funcionan de maravilla.'}},
   'tips':{'en':['Innsbruck airport keeps travel short.','Registry-office slots fill up in summer.','Bring layers &mdash; mountain weather shifts fast.'],
           'de':['Der Flughafen Innsbruck hält die Anreise kurz.','Standesamt-Termine sind im Sommer schnell vergeben.','Zwiebellook &mdash; das Bergwetter wechselt schnell.'],
           'es':['El aeropuerto de Innsbruck acorta el viaje.','Las citas del registro se llenan en verano.','Llevad capas &mdash; el tiempo cambia rápido.']},
   'stories':['official-married-in-the-alps','a-journey-of-love-and-adventure','lake-elopement-tyrol-mountains']},
 'best-alps-elopement-locations':{
   'facts':[('regions',{'en':'Dolomites &amp; Tyrol','de':'Dolomiten &amp; Tirol','es':'Dolomitas y Tirol'}),
            ('access',{'en':'Hike or cable car','de':'Wanderung oder Bergbahn','es':'Senderismo o teleférico'}),
            ('light',{'en':'Sunrise','de':'Sonnenaufgang','es':'Amanecer'})],
   'sec4':{'h':{'en':'How far will you walk?','de':'Wie weit wollt ihr gehen?','es':'¿Cuánto caminaréis?'},
           'p':{'en':'From five-minute strolls to full-day summits &mdash; we match the effort to your comfort, fitness and footwear.',
                'de':'Von fünf Minuten Spaziergang bis zum Ganztags-Gipfel &mdash; wir passen die Anstrengung an Komfort, Kondition und Schuhwerk an.',
                'es':'Desde paseos de cinco minutos hasta cumbres de día entero &mdash; ajustamos el esfuerzo a vuestra comodidad, forma física y calzado.'}},
   'tips':{'en':['Cable cars open big views with little effort.','Lakes are calmest at first light.','Ask us about permit-free spots.'],
           'de':['Bergbahnen bieten große Ausblicke mit wenig Aufwand.','Seen sind im ersten Licht am ruhigsten.','Fragt uns nach genehmigungsfreien Orten.'],
           'es':['Los teleféricos dan grandes vistas con poco esfuerzo.','Los lagos están más tranquilos al amanecer.','Preguntadnos por lugares sin permiso.']},
   'stories':['crystal-clear-water-elopement','intimate-lake-eibsee-elopement','sunset-elopement-tyrol']},
 'how-to-plan-your-elopement':{
   'facts':[('lead',{'en':'3&ndash;9 months','de':'3&ndash;9 Monate','es':'3&ndash;9 meses'}),
            ('guests',{'en':'0&ndash;20','de':'0&ndash;20','es':'0&ndash;20'}),
            ('includes',{'en':'Photo &middot; Film &middot; Planning','de':'Foto &middot; Film &middot; Planung','es':'Foto &middot; Film &middot; Planificación'})],
   'sec4':{'h':{'en':'How far ahead to book','de':'Wie früh buchen','es':'Con cuánta antelación reservar'},
           'p':{'en':'Popular summer dates fill 6&ndash;12 months out; the off-season is often possible on shorter notice.',
                'de':'Beliebte Sommertermine sind 6&ndash;12 Monate im Voraus ausgebucht; in der Nebensaison geht oft auch kurzfristig etwas.',
                'es':'Las fechas populares de verano se llenan con 6&ndash;12 meses; la temporada baja suele ser posible con menos antelación.'}},
   'tips':{'en':['Decide the feeling before the location.','Build in a weather buffer day.','Let us handle permits and vendors.'],
           'de':['Erst das Gefühl, dann den Ort festlegen.','Plant einen Wetter-Puffertag ein.','Überlasst uns Genehmigungen und Dienstleister.'],
           'es':['Decidid la sensación antes que el lugar.','Reservad un día de margen por el clima.','Dejadnos permisos y proveedores.']},
   'stories':['ultimate-italian-elopement','mountain-elopement-dolomiten','pizza-elopement-at-tre-cime-cadini-di-misurina']},
 'most-beautiful-dolomites-spots':{
   'facts':[('regions',{'en':'Dolomites','de':'Dolomiten','es':'Dolomitas'}),
            ('access',{'en':'Cable car or hike','de':'Seilbahn oder Wanderung','es':'Teleférico o caminata'}),
            ('light',{'en':'Sunrise','de':'Sonnenaufgang','es':'Amanecer'})],
   'sec4':{'h':{'en':'How to choose your spot','de':'Wie ihr euren Ort wählt','es':'Cómo elegir el lugar'},
           'p':{'en':'We match the place to your fitness, the season and the mood you want — lakeside calm, ridge-top drama or a quiet meadow.','de':'Wir wählen den Ort nach eurer Kondition, der Jahreszeit und der gewünschten Stimmung — Seeruhe, Grat-Dramatik oder stille Wiese.','es':'Elegimos el lugar según vuestra forma, la estación y el ambiente que buscáis — calma junto al lago, drama en la cresta o un prado tranquilo.'}},
   'tips':{'en':['Go at first light to beat the crowds.','Emerald lakes glow brightest in the morning.','Ask us about permit-free spots.'],
           'de':['Kommt bei erstem Licht, um dem Trubel zu entgehen.','Smaragdseen leuchten morgens am schönsten.','Fragt uns nach genehmigungsfreien Orten.'],
           'es':['Id con la primera luz para evitar la gente.','Los lagos esmeralda brillan más de mañana.','Preguntadnos por lugares sin permiso.']},
   'stories':['lago-di-braies-elopement','sunrise-dolomites-elopement']},
 'helicopter-elopement-dolomites-guide':{
   'facts':[('access',{'en':'By helicopter','de':'Per Helikopter','es':'En helicóptero'}),
            ('season',{'en':'Jun&ndash;Sep','de':'Juni&ndash;Sep','es':'Jun&ndash;Sep'}),
            ('includes',{'en':'Flight &asymp; &euro;2,500+','de':'Flug &asymp; &euro;2.500+','es':'Vuelo &asymp; &euro;2.500+'})],
   'sec4':{'h':{'en':'What can go wrong','de':'Was schiefgehen kann','es':'Qué puede salir mal'},
           'p':{'en':'Only the weather. If the mountain is closed in, we move the flight or switch to a stunning ground location — you never lose the day.','de':'Nur das Wetter. Wenn der Berg dicht ist, verschieben wir den Flug oder wechseln zu einer grandiosen Boden-Location — der Tag ist nie verloren.','es':'Solo el tiempo. Si la montaña está cerrada, movemos el vuelo o cambiamos a una localización espectacular en tierra — nunca perdéis el día.'}},
   'tips':{'en':['Book the widest possible weather window.','Bring layers — a summit is cold.','Keep the group small for the flight.'],
           'de':['Plant ein möglichst breites Wetterfenster.','Zieht euch warm an — am Gipfel ist es kalt.','Haltet die Gruppe für den Flug klein.'],
           'es':['Reservad la ventana de tiempo más amplia posible.','Llevad capas — en la cumbre hace frío.','Mantened el grupo pequeño para el vuelo.']},
   'stories':['adventure-helicopter-elopement-dolomites','mountain-elopement-dolomiten']},
 'mountain-proposal-guide':{
   'facts':[('season',{'en':'Year-round','de':'Ganzjährig','es':'Todo el año'}),
            ('light',{'en':'Sunrise','de':'Sonnenaufgang','es':'Amanecer'}),
            ('lead',{'en':'2&ndash;8 weeks','de':'2&ndash;8 Wochen','es':'2&ndash;8 semanas'})],
   'sec4':{'h':{'en':'And after the yes?','de':'Und nach dem Ja?','es':'¿Y tras el sí?'},
           'p':{'en':'We keep shooting for a relaxed couples session, then send you a few images the same day to share with family.','de':'Wir fotografieren weiter für ein entspanntes Paar-Shooting und schicken euch noch am selben Tag ein paar Bilder für die Familie.','es':'Seguimos fotografiando para una sesión de pareja relajada y os enviamos unas imágenes el mismo día para compartir con la familia.'}},
   'tips':{'en':['Pick a spot with a natural reason to pause.','Keep the ring somewhere secure on the walk.','Tell us the signal so we\'re ready.'],
           'de':['Wählt einen Ort mit natürlichem Grund für eine Pause.','Verstaut den Ring auf dem Weg sicher.','Nennt uns das Signal, damit wir bereit sind.'],
           'es':['Elegid un lugar con motivo natural para parar.','Guardad el anillo seguro en la caminata.','Decidnos la señal para estar listos.']},
   'stories':['mountain-engagement','a-journey-of-love-and-adventure']},
 'sunrise-or-sunset-elopement':{
   'facts':[('light',{'en':'Golden hour','de':'Goldene Stunde','es':'Hora dorada'}),
            ('season',{'en':'Jun&ndash;Oct','de':'Juni&ndash;Okt','es':'Jun&ndash;Oct'}),
            ('diff',{'en':'Easy&ndash;Moderate','de':'Leicht&ndash;Moderat','es':'Fácil&ndash;Moderado'})],
   'sec4':{'h':{'en':'Our honest take','de':'Unsere ehrliche Meinung','es':'Nuestra opinión sincera'},
           'p':{'en':'If you can face the early alarm, sunrise wins almost every time — the light and the solitude are worth it. Sunset is the relaxed, reliable choice.','de':'Wenn ihr den frühen Wecker schafft, gewinnt der Sonnenaufgang fast immer — Licht und Ruhe sind es wert. Der Sonnenuntergang ist die entspannte, sichere Wahl.','es':'Si podéis con el madrugón, el amanecer gana casi siempre — la luz y la soledad lo valen. El atardecer es la opción relajada y segura.'}},
   'tips':{'en':['Sunrise: scout the trail the day before.','Sunset: start earlier than you think.','Either way, stay for blue hour.'],
           'de':['Sonnenaufgang: erkundet den Weg am Vortag.','Sonnenuntergang: startet früher als gedacht.','So oder so: bleibt zur blauen Stunde.'],
           'es':['Amanecer: explorad el sendero la víspera.','Atardecer: empezad antes de lo que creéis.','En ambos casos: quedaos a la hora azul.']},
   'stories':['sunrise-dolomites-elopement','sunset-elopement-tyrol']},
 'elopement-things-nobody-tells-you':{
   'facts':[('lead',{'en':'Plan early','de':'Früh planen','es':'Planificad pronto'}),
            ('guests',{'en':'0&ndash;20','de':'0&ndash;20','es':'0&ndash;20'}),
            ('includes',{'en':'Vows &middot; layers &middot; snacks','de':'Gelübde &middot; Schichten &middot; Snacks','es':'Votos &middot; capas &middot; snacks'})],
   'sec4':{'h':{'en':'The one thing to remember','de':'Das Eine, das ihr behalten solltet','es':'Lo único que recordar'},
           'p':{'en':'It\'s your day, not a photo shoot. The best images come when you forget we\'re there and simply be together — we plan the rest around that.','de':'Es ist euer Tag, kein Fotoshooting. Die besten Bilder entstehen, wenn ihr uns vergesst und einfach zusammen seid — den Rest planen wir darum herum.','es':'Es vuestro día, no una sesión. Las mejores imágenes surgen cuando os olvidáis de que estamos y simplemente estáis juntos — el resto lo planeamos alrededor.'}},
   'tips':{'en':['Print your vows — screens fail in the cold.','Pack snacks, water and warm layers.','Leave buffer time so nothing feels rushed.'],
           'de':['Druckt euer Gelübde — Displays versagen bei Kälte.','Packt Snacks, Wasser und warme Schichten ein.','Plant Puffer, damit nichts hetzt.'],
           'es':['Imprimid los votos — las pantallas fallan con el frío.','Llevad snacks, agua y capas de abrigo.','Dejad margen para que nada vaya con prisa.']},
   'stories':['mountain-elopement-dolomiten','ultimate-italian-elopement']},
}

# ================= ITALIAN OVERLAY =================
IT_NAV={'welcome':'Inizio','howto':'Guida','stories':'Storie','packages':'Prezzi','team':'Team','contact':'Contatti'}
IT={
 'ty_k':'Richiesta ricevuta','ty_h':'Grazie',
 'ty_p':'Abbiamo ricevuto il vostro messaggio e vi risponderemo entro 48 ore.',
 'ty_home':'Torna alla home',
 'booking':'Prenotazioni 2027 &middot; date 2028','booking_link':'su richiesta',
 'f_tag':'Fotografia e pianificazione editoriale di elopement nelle Dolomiti e nelle Alpi.',
 'f_explore':'Esplora','f_team':'Il nostro team','f_role_photo':'Foto','f_role_plan':'Pianificazione','f_role_film':'Film','f_role_mua':'Trucco',
 'f_imprint':'Note legali','f_privacy':'Privacy','view_all':'Tutte le storie','start_planning':'Iniziamo a pianificare',
 'get_in_touch':'Contattaci','visit':'Visita','request':'Richiedi','tm_kick':'Il Dream Team','tm_over':'Dietro il vostro giorno',
 'tm_h':'Il team dietro<br>il vostro elopement','tm_r1':'Pianificazione e coordinamento','tm_r2':'Film di elopement','tm_r3':'Trucco e acconciatura',
 'tm_d1':'La nostra planner nelle Dolomiti &mdash; logistica, permessi, alloggio e ogni dettaglio gestito sul posto, così potete semplicemente esserci. Con anni di esperienza e cresciuta nel cuore delle Dolomiti, conosce ogni pietra &mdash; il che crea un’atmosfera splendidamente rilassata.',
 'tm_d2':'Film di elopement cinematografici che custodiscono il movimento, il suono e l’emozione del vostro giorno &mdash; il complemento in movimento alle fotografie.',
 'tm_d3':'Trucco e acconciatura da sposa naturali e duraturi, pensati per vento, quota e prima luce in montagna &mdash; voi, al vostro massimo splendore.',
 'tm_rp':'Fotografia e regia',
 'tm_dp':'Fondatore e fotografo principale &mdash; tirolese, a casa tra Innsbruck e le Dolomiti. Premiato (Way Up North Awards 2024), pubblicato su Rangefinder. Andreas accompagna ogni coppia verso la luce e racconta la giornata come si sente davvero.',
 'bts_k':'Sul posto','bts_over':'Dietro le quinte','bts_h':'Con le nostre coppie,<br>tra le montagne',
 'h_sub':'Matrimoni intimi in montagna nelle Dolomiti e nelle Alpi &mdash; solo voi due, una vetta e una storia da raccontare.',
 'h_btn':'Iniziate la vostra storia','h_h1':'Avventura<br>sopra le nuvole',
 'ms1':'<b>Sede</b> Tirolo &middot; Dolomiti','ms2':'<b>Elopement</b> Fotografia e Film','ms3':'<b>Pianificazione</b> Su misura','ms4':'<b>Dal</b> 2019',
 'mission_k':'La nostra missione','mission_h':'Creiamo il vostro<br>elopement perfetto',
 'mission_lead':'<em>to elope</em> &mdash; sfuggire all’ordinario e sposarsi dove il mondo diventa <em>silenzio</em>.',
 'mission_p1':'Progettiamo matrimoni intimi che riflettono la vostra storia d’amore unica. Se volete rinunciare a location sfarzose e lunghe liste di invitati, avete trovato il vostro partner. Celebriamo l’individualità intrecciando un romanticismo senza tempo in ogni elopement che creiamo.',
 'mission_p2':'Da laghi cristallini a vette innevate e prati tranquilli, le nostre location selezionate in tutta Europa sono scelte per la vostra visione &mdash; e vi accompagniamo a ogni passo.',
 'mission_link':'Come funziona &rarr;','cap_seceda':'Alba sulla cresta del Seceda, Alto Adige.',
 'sel_k':'Lavori scelti','sel_h':'Storie recenti','fig1':'Elopement','fig2':'Cerimonie','fig3':'m sul livello del mare','fig4':'Tazze di caffè',
 'kw_k':'Testimonianze','kw_q':'"La loro conoscenza del territorio è stata preziosissima. Ci hanno consigliato la vetta perfetta e hanno reso il nostro giorno magico davvero indimenticabile."',
 'kw_who':'Aubrey e Matt &mdash; Dolomiti, 2024','cta_k':'Contatti','cta_h':'La vostra avventura è<br>a una conversazione di distanza',
 'diff_k':'Perché noi','diff_h':'Ciò che ci rende diversi',
 'diff1_h':'Full-service, davvero completo',
 'diff1_p':'Pianificazione, permessi, fiori, torta, cerimonia, fotografia e film &mdash; un team locale, un unico referente. Voi arrivate, di tutto il resto ci siamo occupati noi.',
 'diff2_h':'Epico senza la salita',
 'diff2_p':'Dagli elopement in elicottero sopra le Dolomiti a location selezionate raggiungibili in funivia: creiamo giornate mozzafiato per coppie che desiderano l’emozione della vetta &mdash; con o senza la camminata di sei ore.',
 'diff3_h':'Sposati legalmente, in vetta alla montagna',
 'diff3_p':'Da austriaci, sappiamo come rendere il vostro matrimonio in montagna legalmente valido &mdash; con un ufficiale di stato civile in vetta. Cerimonia vera, certificato vero, montagne vere. (Le cerimonie simboliche nelle Dolomiti italiane sono, naturalmente, altrettanto belle.)',
 'diff4_h':'Nati qui, a casa qui',
 'diff4_p':'Un piccolo team locale, a casa tra Innsbruck e le Dolomiti &mdash; la planner Jlenia, il fotografo Andreas e la filmmaker Stefanie. Premiati: Way Up North Awards 2024.',
 'award_lbl':'Premiati','pub_lbl':'Pubblicato in',
 'aw_k':'Riconoscimenti','aw_h':'Premiati e menzionati','aw_lead':'Prenotare un matrimonio tra montagne che non avete mai calpestato richiede fiducia. Negli anni il nostro lavoro è stato premiato e pubblicato da chi le coppie prendono come riferimento.','aw_qual':'Qualifica','aw_feat':'Menzionato','aw_member':'Membro','aw_wun':'Vincitore &mdash; Best Epic Portrait','aw_jb':'I migliori d&rsquo;Austria','aw_fl':'Fotografo in elenco','aw_rf':'Rf Photo of the Day',
 'ht_k':'Guida','ht_h1':'Elopement nelle<br>Dolomiti','ht_s1k':'Da dove iniziare','ht_s1h':'Unire avventura<br>e romanticismo',
 'ht_s1p1':'Curiosi di progettare un elopement che unisca avventura e romanticismo nelle splendide Dolomiti? La nostra specialità è creare elopement di montagna indimenticabili, su misura per la vostra visione.',
 'ht_s1p2':'Iniziamo aiutandovi a scegliere la location perfetta &mdash; considerando accessibilità, paesaggio e atmosfera desiderata. Che sogniate di scambiarvi le promesse su una vetta appartata o in riva a un lago alpino, ogni dettaglio ruota attorno a voi due.',
 'ht_s1p3':f'Quando il giorno richiede più mani, lavoriamo con una cerchia fidata: pianificazione sul posto di <a class="partner-inline" href="{P_PLAN[1]}" target="_blank" rel="noopener">Dolomites Wedding Planner</a>, fotografia di <a class="partner-inline" href="https://hochzeitsfotograf.tirol" target="_blank" rel="noopener">Blitzkneisser</a>.',
 'ht_cap':'Un mattino silenzioso sopra il limite del bosco.','ht_e_k':'L’essenziale','ht_e_h':'Cosa considerare',
 'ht_step1t':'Scegliere la location','ht_step1p':'Vetta, lago, prato o cresta &mdash; scegliamo lo scenario in base alla vostra visione, alla stagione e a quanto volete camminare.',
 'ht_step2t':'Pianificare il giorno','ht_step2p':'Un programma rilassato, la luce migliore, un piano flessibile per il meteo e tutta la logistica &mdash; trasferimenti, fiori, trucco e acconciatura.',
 'ht_step3t':'Le vostre promesse','ht_step3p':'Promesse personali, un celebrante o una cerimonia civile opzionale, e una fotografia che cattura tutto esattamente come si è sentito.',
 'ht_ready':'Iniziamo','ht_cta_h':'Iniziamo a pianificare<br>la vostra fuga in montagna',
 'st_k':'L’archivio','st_h':'Storie','st_lead':'Uno sguardo alle avventure che abbiamo avuto l’onore di immortalare &mdash; promesse in vetta, la prima luce sulle creste e momenti di quiete sopra le nuvole.',
 'st_cta_k':'La vostra storia','st_cta_h':'La prossima<br>sarà la vostra?','cat_k':'Categoria','cat_lead':'Storie di elopement nella categoria <em>{x}</em>.',
 'pi_lead':'Un solo giorno, dall’inizio alla fine &mdash; la salita, la luce, il sereno scambio delle promesse e il lungo cammino di ritorno.',
 'pi_p':'Ecco il loro mattino sopra le nuvole, esattamente come si è svolto.','pi_your':'Lo sognate anche voi?','pi_cta_h':'Troviamo<br>la vostra vetta',
 'pi_gallery':'Il giorno in immagini',
 'pi_outro':'Comunque immaginiate la vostra giornata &mdash; un&rsquo;alba silenziosa, una vetta, un lago tutto per voi &mdash; la pianifichiamo intorno a voi due e la fotografiamo com&rsquo;è stata davvero.',
 'pi_vplan':'Pianificazione','pi_vfilm':'Film','pi_vmua':'Trucco',
 'pk_k':'Investimento','pk_h':'Prezzi','pk_lead':'I nostri pacchetti sono un punto di partenza, non un limite. Che sogniate un matrimonio di tre giorni in elicottero o una semplice cerimonia in vetta &mdash; solo il cielo è il limite.',
 'pk_t1':'express elopement','pk_t2':'the elopement','pk_t3':'micro wedding','pk_l1':'Base','pk_l2':'Popolare','pk_l3':'Tutto',
 'pk_hours':'ore di copertura','pk_photos':'foto',
 'pk_note':f'La pianificazione completa e il coordinamento sul posto sono realizzati insieme al nostro partner <a class="partner-inline" href="{P_PLAN[1]}" target="_blank" rel="noopener">Dolomites Wedding Planner</a> &mdash; Mountain Elopement resta il vostro unico punto di riferimento.',
 'pk_addk':'Qualcosa di ancora più speciale?','pk_cta_h':'Costruite il vostro<br>pacchetto elopement su misura','pk_req_price':'Richiedi i prezzi',
 'pk_band_k':'Come lavoriamo','pk_band_q':'"I nostri prezzi sono un assaggio del possibile. Ogni coppia ha la propria visione e il proprio budget &mdash; per questo adattiamo ogni pacchetto ai vostri desideri."',
 'pk_next':'Pianifichiamo','ad_heli':'Elicottero','ad_film':'Film &middot; 1&ndash;2 min','ad_civil':'Cerimonia civile','ad_celeb':'Celebrante',
 'ad_cake':'Torta','ad_music':'Musicisti','ad_mua':'Trucco e acconciatura','ad_backdrop':'Backdrop e fiori','ad_from':'da','ad_onreq':'su richiesta',
 'tp_k':'Le persone','tp_h':'Il nostro team','tp_lead':'Un elopement di montagna richiede una piccola cerchia fidata. Ecco le persone che rendono possibile il vostro giorno &mdash; dal primo scatto all’ultimo dettaglio.',
 'tp_fk':'Il team principale','tp_flead':'Mountain Elopement &mdash; un piccolo team locale dietro la vostra giornata.',
 'tp_fp1':'Siamo un piccolo team locale, a casa nelle Dolomiti e nelle Alpi &mdash; guidato dalla planner Jlenia e dal fotografo Andreas. Da anni accompagniamo le coppie verso vette silenziose e laghi nascosti, catturando il giorno esattamente come si sente &mdash; senza pose, senza fretta, autentico.',
 'tp_fp2':'Insieme pianifichiamo e fotografiamo l&rsquo;intera vostra giornata &mdash; e dove la rende ancora più bella, coinvolgiamo una cerchia fidata.',
 'tp_hello':'Salutateci &rarr;','tp_cta_k':'Un team','tp_cta_h':'Tutto ciò che serve,<br>da un’unica mano','tp_plan':'Pianificate il vostro giorno',
 'ct_k':'Salutateci','ct_h':'Contatti','ct_lead':'Non vediamo l’ora di ascoltare la vostra storia! Raccontateci le vostre idee &mdash; e vi aiuteremo a rendere realtà il vostro elopement da sogno.',
 'ct_details':'I vostri dati','ct_name':'Nome','ct_name_ph':'Il vostro nome','ct_email':'Email','ct_date':'Data elopement (circa)','ct_date_ph':'es. giugno 2027',
 'ct_dream':'Cosa sognate?','ct_story':'Raccontateci la vostra storia','ct_story_ph':'Dove, quando e cosa immaginate...','ct_send':'Invia richiesta',
 'ct_note':'Modulo prototipo &mdash; nella versione finale si collega all’email (es. Formspree).','ct_based':'Sede','ct_based_v':'Tirolo e Dolomiti',
 'ct_sending':'Invio in corso…','ct_ok':'Inviato — grazie!','ct_err':'Qualcosa è andato storto. Riprova o scrivici direttamente.',
 'chips':['Foto','Film','Backdrop','Fiori','Trucco','Elicottero','Escursione','Musica'],
 'lg_k':'Note legali','lg_imprint':'Note legali','lg_privacy':'Informativa privacy','lg_lead':'Segnaposto &mdash; il testo esistente verrà trasferito invariato dal sito attuale.',
 'hero_inq':'Richiesta diretta','hero_guides':'Guide','hero_price':'Prezzi','film_k':'Il film',
 'gd_k':'La guida','gd_h':'Guide',
 'ht_start':'Inizia qui','ht_start_copy':'Un punto di partenza sereno per chi pianifica un elopement nelle Dolomiti o un matrimonio intenzionale in montagna &mdash; e vuole capire meglio da dove cominciare.',
 'guides_k':'Guide di pianificazione','guides_h':'Guide per pianificare il tuo elopement','guides_intro':'Guide pratiche e sincere per pianificare un elopement nelle Alpi e nelle Dolomiti.',
 'read_guide':'Leggi la guida','guide_kick':'Guida','more_guides':'Altre guide','map_k':'La regione','map_h':'Dove vi sposerete?','map_hint':'Tocca una regione',
 'map_tyrol':'Tirolo','map_lakes':'Laghi alpini','map_dol':'Dolomiti','cats_k':'Per tema','cats_h':'Esplora per categoria',
 'quick_facts':'In breve','good_to_know':'Buono a sapersi','related_stories':'Elopement reali',
}
IT_LBL={'season':'Periodo migliore','diff':'Difficoltà','reach':'Come arrivare','regions':'Regioni','access':'Accesso','light':'Luce migliore','lead':'Preavviso','guests':'Ospiti','includes':'Include'}
IT_CATS={'couple':'Coppie','dolomites':'Dolomiti','mountain':'Montagna','lake':'Laghi','elopement':'Elopement','engagement':'Fidanzamento'}
IT_ST={'climbing-wedding':'Matrimonio di arrampicata sulle cime delle Dolomiti','sunrise-elopement-in-the-dolomites':'Un magico elopement all’alba nelle Dolomiti','mountain-engagement':'Proposta in vetta &mdash; fidanzamento in montagna','crystal-clear-water-elopement':'Elopement di montagna presso acque cristalline','hiking-elopement-lagazuoi-dolomites':'Un matrimonio d’inverno in Val Gardena','pizza-elopement-at-tre-cime-cadini-di-misurina':'Elopement con pizza alle Tre Cime','mountain-elopement-dolomiten':'Elopement nelle Dolomiti in tre location','sunrise-dolomites-elopement':'Alba nelle Dolomiti','official-married-in-the-alps':'Matrimonio ufficiale sulla cima del Tirolo','ultimate-italian-elopement':'Un elopement in tre giorni','adventure-helicopter-elopement-dolomites':'Elopement d’avventura in elicottero nelle Dolomiti','lake-elopement-tyrol-mountains':'Elopement al lago','a-journey-of-love-and-adventure':'Un elopement sugli sci nelle Dolomiti d’inverno','couple-shoot-photo':'Servizio di coppia in autunno','sunset-elopement-tyrol':'Elopement al tramonto in vetta','intimate-lake-eibsee-elopement':'Elopement intimo al lago Eibsee','lago-di-braies-elopement':'Elopement al Lago di Braies','rainy-lago-di-braies-pizza-elopement':'Barche a remi e pizza al Lago di Braies &mdash; un elopement'}
IT_TITLES={'home':'Mountain Elopement — Dove l’avventura incontra il romanticismo','howto':'Elopement nelle montagne d’Europa — Mountain Elopement','stories':'Storie — Mountain Elopement','packages':'Prezzi — Mountain Elopement','team':'Il nostro team e i partner — Mountain Elopement','contact':'Contatti — Mountain Elopement','thankyou':'Grazie per la vostra richiesta — Mountain Elopement'}
IT_DESC={'home':'Fotografia e pianificazione editoriale di elopement nelle Dolomiti e nelle Alpi.','howto':'Una guida per il vostro elopement nelle Dolomiti e nelle Alpi.','stories':'Storie di elopement di montagna nelle Dolomiti e nelle Alpi.','packages':'Pacchetti elopement: fotografia, pianificazione, film, fiori e trucco.','team':'Il team dietro il vostro elopement — fotografia, pianificazione, film e trucco.','contact':'Raccontateci la vostra storia. Fotografia e pianificazione di elopement nelle Dolomiti e nelle Alpi.','thankyou':'Grazie — abbiamo ricevuto la vostra richiesta.'}
IT_GUIDES={
 'dolomites-elopement-guide':{'title':'Elopement nelle Dolomiti','excerpt':'Tutto ciò che serve per sposarvi tra le cime più belle d’Italia.','intro':'Le Dolomiti sono uno dei luoghi più mozzafiato d’Europa per un elopement &mdash; cime drammatiche, laghi turchesi e una luce che tinge la roccia di rosa all’alba. Ecco come rendere il vostro giorno qui semplice.','sec':[('Periodo migliore','Da fine giugno a settembre il tempo è stabile e i rifugi aperti. Per meno folla e larici dorati, pianificate a fine settembre.'),('Dove scambiarvi le promesse','Dalle creste del Seceda alle rive del Lago di Braies e alle Tre Cime, vi aiutiamo a scegliere un luogo adatto alla vostra forma fisica e alla vostra visione.'),('Renderlo ufficiale','In Italia potete sposarvi legalmente con qualche pratica in anticipo, oppure celebrare una cerimonia simbolica e completare la parte legale a casa. Vi indichiamo la strada giusta.'),('Come arrivare: passi, strade a pedaggio e funivie','La maggior parte delle coppie atterra a Venezia, Verona o Innsbruck e guida l\'ultimo tratto. I grandi passi &mdash; Giau, Falzarego e Pordoi &mdash; sono gratuiti e panoramici, ma due luoghi hanno un costo o limitazioni: la strada a pedaggio delle Tre Cime di Lavaredo sopra Misurina (circa 30&ndash;45&nbsp;&euro; ad auto in stagione) sale quasi sotto le cime, e il Lago di Braies limita il traffico estivo verso il lago dalle 10 alle 16 circa, perciò lì fotografiamo alla prima luce. Dove finisce la strada spesso inizia una funivia &mdash; Seceda sopra Ortisei, Lagazuoi dal Passo Falzarego, Sass Pordoi dal Passo Pordoi. Guardate [[g:most-beautiful-dolomites-spots|i nostri luoghi preferiti delle Dolomiti]] per sapere dove porta ciascuna.'),('Dove alloggiare','Cortina d\'Ampezzo, Ortisei in Val Gardena e i paesi dell\'Alta Badia sono le basi più comode &mdash; a un\'ora dai luoghi principali e pieni di rifugi per una cena di nozze. Per una cerimonia all\'alba prenotiamo spesso un rifugio, così dormite in montagna e vi svegliate già lì; un esempio reale è [[s:sunrise-dolomites-elopement|questo albeggiare nelle Dolomiti]], e [[g:sunrise-or-sunset-elopement|alba o tramonto?]] vi aiuta a scegliere la luce.')]},
 'elope-in-austria':{'title':'Elopement in Austria e Tirolo','excerpt':'Laghi alpini, alte creste e un matrimonio legale semplice.','intro':'Il Tirolo è casa nostra. Dalle cime sopra Innsbruck ai laghi nascosti, l’Austria rende l’elopement semplice &mdash; anche dal punto di vista legale.','sec':[('Matrimonio legale in Austria','L’Austria consente cerimonie ufficiali in municipio e, in alcune regioni, in splendide location all’aperto. Coordiniamo appuntamento e pratiche.'),('Location migliori','La Nordkette sopra Innsbruck, la Zillertal e innumerevoli laghi alpini sono facilmente raggiungibili.'),('Come arrivare','Innsbruck ha un proprio aeroporto e collegamenti rapidi con Monaco e Venezia, il che rende il Tirolo una delle regioni alpine più accessibili.'),('Funivie e strade a pedaggio alpine','Innsbruck è l\'unica città delle Alpi con l\'alta montagna alla porta: la funicolare Hungerburgbahn e le funivie della Nordkette vi portano dal centro storico all\'Hafelekar, a 2.256&thinsp;m, in circa venti minuti. Più all\'interno, due strade a pedaggio aprono acque turchesi &mdash; la Schlegeis Alpenstraße in Zillertal (circa 13&nbsp;&euro; ad auto) termina a un bacino azzurro latte, e le strade d\'alta quota di Kühtai e Timmelsjoch salgono ben oltre il limite del bosco. Grandi scenari alpini quasi senza camminare.'),('Dove amiamo scambiare le promesse in Tirolo','La nostra rosa: il protetto Obernberger See presso il Brennero, lo smeraldo Schlegeisspeicher in Zillertal e i quieti laghetti d\'alta quota sopra Kühtai. Tutti vicini a Innsbruck eppure in un altro mondo &mdash; una vera giornata tirolese è [[s:lake-elopement-tyrol-mountains|questo elopement al lago alpino]], oppure, se lo volete legale in vetta, [[s:official-married-in-the-alps|un ufficiale di stato civile vero in montagna]]. Altri preferiti in [[g:best-alps-elopement-locations|le nostre migliori location alpine]].')]},
 'best-alps-elopement-locations':{'title':'Le migliori location per elopement nelle Alpi','excerpt':'Le nostre vette, laghi e prati preferiti per un giorno indimenticabile.','intro':'Dopo anni in montagna, questi sono i luoghi in cui torniamo di continuo &mdash; ognuno con il proprio carattere e la propria luce.','sec':[('Per gli amanti delle vette','Alte creste e cime per le coppie che cercano la fatica &mdash; e la ricompensa &mdash; di stare in cima.'),('Per gli amanti dell’acqua','Laghi alpini turchesi come Braies, Eibsee e specchi d’acqua tirolesi nascosti per mattine calme e immobili.'),('Per chi ama la calma','Prati dolci e punti panoramici raggiungibili in funivia, quando preferite non camminare troppo.'),('Laghi per cui vale la pena alzarsi presto','Per alcuni laghi alpini vale la pena puntare la sveglia. Il Lago di Braies è l\'icona smeraldo con la casetta e le barche; il Lago di Sorapis brilla turchese latte dopo due ore di cammino dal Passo Tre Croci (non lo raggiunge alcuna auto); il Lago di Federa siede in una corona di larici che a ottobre si tingono d\'oro; e l\'Eibsee sotto lo Zugspitze nasconde insenature boscose che in pochi trovano. Tutti più quieti alla prima luce &mdash; guardateli nei [[c:lake|nostri elopement al lago]], compreso [[s:rainy-lago-di-braies-pizza-elopement|un mattino di pioggia a Braies]].'),('Punti panoramici in funivia senza salita','Se preferite non camminare molto in abito, ci pensano gli impianti. La funivia del Seceda vi posa su una cresta erbosa inclinata sopra la Val Gardena; il Sass Pordoi &mdash; la &ldquo;terrazza delle Dolomiti&rdquo; &mdash; vi porta a 2.950&thinsp;m in pochi minuti; il Lagazuoi apre un balcone su mezza catena; e la Nordkette sopra Innsbruck è a venti minuti dalla città. Programmiamo la prima o l\'ultima cabina perché il belvedere sia quasi deserto &mdash; di più su ciascuno nei [[g:most-beautiful-dolomites-spots|luoghi più belli delle Dolomiti]].')]},
 'how-to-plan-your-elopement':{'title':'Come pianificare il vostro elopement di montagna','excerpt':'Una tabella di marcia semplice e senza stress, dall’idea al “sì”.','intro':'Pianificare un elopement è molto più semplice di un grande matrimonio &mdash; ma poche decisioni iniziali fanno scorrere tutto. Ecco la versione breve.','sec':[('1 · Prima la sensazione, poi il luogo','Volete avventura e fatica, o calma e semplicità? Questa risposta ci indica la regione e la location giuste.'),('2 · Scegliete stagione e periodo','Inseriamo un margine per il meteo, per poter spostare il vostro giorno di qualche ora o di un giorno secondo le condizioni.'),('3 · Al resto pensiamo noi','Permessi, programma, fiori, trucco e acconciatura, trasferimenti e la parte legale &mdash; tutto gestito con i nostri partner.'),('Permessi, accessi e i piccoli costi','Oltre alle voci principali, una giornata in montagna ha piccoli costi facili da dimenticare. Alcune location richiedono un permesso foto o cerimonia; la strada a pedaggio delle Tre Cime costa circa 30&ndash;45&nbsp;&euro; ad auto; il Lago di Braies ha una finestra d\'accesso estiva e parcheggio a pagamento; anche i biglietti della funivia e una notte in rifugio si sommano. Nulla di costoso &mdash; serve solo pianificazione, che facciamo noi per voi. Quelli di cui nessuno vi avverte sono in [[g:elopement-things-nobody-tells-you|ciò che nessuno vi dice sull\'elopement]].'),('Una giornata che non sembra mai di fretta','Una tipica giornata all\'alba inizia al buio: trucco e acconciatura, un breve trasferimento o una funivia, poi le promesse quando la prima luce tocca la roccia. Seguono i ritratti con i sentieri ancora deserti, una lunga colazione in rifugio e il tempo semplicemente di essere sposati. Inseriamo un margine &mdash; spesso un giorno di riserva &mdash; perché il meteo non imponga mai la fretta. Indecisi tra prima e ultima luce? Leggete [[g:sunrise-or-sunset-elopement|alba o tramonto?]], o guardate un\'intera giornata senza fretta in [[s:ultimate-italian-elopement|questo elopement italiano di tre giorni]].')]},
 'most-beautiful-dolomites-spots':{'title':'I luoghi più belli delle Dolomiti','excerpt':'Le nostre vette, laghi e creste preferiti per un elopement indimenticabile.','intro':'Dopo anni a fotografare qui, alcuni luoghi ci richiamano sempre &mdash; ognuno con la sua luce, la sua atmosfera e il suo impegno. Ecco i nostri preferiti e come sceglierli.','sec':[('Lago di Braies e i grandi laghi','Acqua smeraldo, l’antica casetta delle barche e cime che salgono dalla riva. Braies è iconico &mdash; e all’alba, prima delle barche, meravigliosamente quieto.'),('Seceda, Tre Cime e le alte creste','Per pura spettacolarità, nulla batte le creste frastagliate. Alcune a pochi minuti di funivia, altre una vera escursione &mdash; scegliamo il luogo in base a quanto volete camminare.'),('Laghi nascosti per gli avventurosi','Lontano dalle icone, l\'acqua più quieta ripaga una camminata. Il Lago di Sorapis brilla di un turchese latte irreale a un paio d\'ore dal Passo Tre Croci; il Lago di Federa specchia la Croda da Lago in una corona di larici; il piccolo Lago di Limides cattura le Tofane accanto al Passo Falzarego; e il Lago d\'Antorno, sulla strada, incornicia le guglie dei Cadini senza alcuno sforzo. Sono i luoghi per chi vuole la bellezza di Braies senza la sua folla &mdash; e si fotografano splendidi con ogni tempo, come mostra [[s:pizza-elopement-at-tre-cime-cadini-di-misurina|questa giornata vicino alle Tre Cime]].'),('Passi, prati e le Cinque Torri','Per grandi scenari quasi raggiungibili in auto, gli alti passi sono difficili da battere. Il Passo Giau è un anfiteatro di prati nella corona delle cime; le Cinque Torri &mdash; cinque rocce a forma di torre, con una breve seggiovia da Bai de Dones &mdash; offrono un palco intimo con una storia della Grande Guerra; e i rifugi Averau e Nuvolau sopra di esse servono la cena con vista a 360&deg;. Questi luoghi sulla strada o serviti da impianto sono perfetti se preferite risparmiare le gambe per ballare &mdash; e magnifici sia [[g:sunrise-or-sunset-elopement|all\'alba sia al tramonto]].'),('Come raggiungere ciascuno','L\'accesso decide il vostro mattino. Braies limita il traffico estivo verso il lago dalle 10 alle 16 circa, perciò andiamo prima; la strada a pedaggio delle Tre Cime (circa 30&ndash;45&nbsp;&euro; ad auto) vi porta quasi alla base; Seceda, Lagazuoi e Faloria sono funivie; Sorapis e Federa sono escursioni senza accesso in auto. Pianifichiamo percorso, biglietti e tempi attorno a tutto questo &mdash; l\'intera logistica è in [[g:how-to-plan-your-elopement|come pianificare il vostro elopement]].')]},
 'helicopter-elopement-dolomites-guide':{'title':'La guida all’elopement in elicottero','excerpt':'Come sposarsi su una vetta quasi irraggiungibile &mdash; dall’alto.','intro':'Un elicottero trasforma un trekking di giorni in minuti e vi posa dove la folla non arriva. Ecco come funziona davvero, quanto costa e cosa aspettarvi.','sec':[('Come si svolge la giornata','Volate da un’elisuperficie a valle a un lembo remoto o a un ghiacciaio, vi scambiate le promesse con l’intera catena sotto di voi e tornate &mdash; spesso con tempo per una seconda location. Il volo stesso diventa parte della storia.'),('Costi e pianificazione','Prevedete da circa €2.500 per il volo, secondo il punto di atterraggio e l’orario. Il meteo decide tutto, perciò teniamo sempre una finestra flessibile &mdash; e un bellissimo piano B a terra.'),('Dove può portarvi un elicottero','Un volo apre terreni che un elopement normale non raggiunge mai: un lembo di roccia remoto, un plateau glaciale sulla Marmolada, una vetta che altrimenti sarebbe una salita di due giorni. Gli atterraggi sono effettuati da operatori alpini autorizzati su siti approvati, di solito una breve sosta per cerimonia e ritratti prima del rientro. Il volo stesso diventa metà della storia &mdash; guardatelo nel [[s:adventure-helicopter-elopement-dolomites|nostro elopement in elicottero]].'),('Elicottero, funivia o escursione?','Il volo è il modo più audace per salire, ma non l\'unico. Se volete la sensazione della vetta senza il prezzo, una funivia al Lagazuoi, al Sass Pordoi o al Seceda regala un panorama enorme al costo di un biglietto; se volete che la giornata sia conquistata, un\'escursione dona solitudine e non costa nulla. Spesso li combiniamo &mdash; arrivare in volo, camminare fino a un lembo più quieto. Valutate panorama e fatica nei [[g:most-beautiful-dolomites-spots|luoghi più belli]] e il budget in [[g:how-to-plan-your-elopement|come pianificare]].')]},
 'mountain-proposal-guide':{'title':'Come organizzare una proposta in montagna','excerpt':'Che la sorpresa riesca &mdash; e venga immortalata mentre accade.','intro':'Una proposta in montagna è metà logistica e metà emozione. Ecco come vi aiutiamo a scegliere il momento, mantenere il segreto e fotografarlo senza che il partner ci noti.','sec':[('Scegliere il momento','La prima luce è la nostra preferita: sentieri quieti, colori morbidi e quasi nessuno. Cerchiamo un punto con una pausa naturale &mdash; una vetta, un belvedere, una riva &mdash; dove inginocchiarsi sia naturale.'),('Mantenere il segreto','Organizziamo tutto via messaggio, fotografiamo da lontano con il teleobiettivo e ci confondiamo tra gli escursionisti fino al sì. Dopo restiamo per un vero servizio di coppia per festeggiare.'),('Luoghi che rendono facile la sorpresa','I posti migliori per la proposta hanno un motivo naturale per fermarsi e poca fatica &mdash; una lunga camminata sudata tende a tradire il piano. I belvedere in funivia sono ideali: la cresta del Seceda, la terrazza del Sass Pordoi o la Nordkette a pochi minuti da Innsbruck. Così i laghi sulla strada come la passerella del Lago di Braies o il piccolo Lago d\'Antorno. Andate alla prima luce e avrete la ringhiera tutta per voi. Scegliete tra [[g:best-alps-elopement-locations|le nostre migliori location alpine]].'),('L\'anello, il meteo e un piano B','Tenete l\'anello in una tasca chiusa e sicura durante il cammino &mdash; non in una giacca che potreste porgere. La prima luce regala sentieri vuoti e colori morbidi, ma il meteo di montagna cambia in fretta, perciò teniamo sempre un luogo di riserva e un mattino di scorta. Dopo il sì continuiamo per un servizio di coppia rilassato e possiamo consegnare qualche immagine lo stesso giorno. Poi si festeggia &mdash; un vero bagliore del giorno dopo è [[s:mountain-engagement|questo fidanzamento in montagna]].')]},
 'sunrise-or-sunset-elopement':{'title':'Alba o tramonto per il vostro elopement?','excerpt':'Due giornate molto diverse &mdash; ecco come scegliere la vostra luce.','intro':'La stessa vetta sembra due luoghi diversi all’alba e al tramonto. La scelta plasma l’intera giornata &mdash; la fatica, la folla e l’atmosfera. Ecco come vi aiutiamo a decidere.','sec':[('Alba: solitudine e luce morbida','Una partenza prima dell’alba vi regala sentieri deserti e l’enrosadira rosa prima che la valle si svegli. Richiede una sveglia presto e strati caldi &mdash; ma la quiete non ha eguali.'),('Tramonto: caldo e senza fretta','L’ora d’oro è più comoda &mdash; niente sveglia, salita lenta e luce calda che resta. In cambio c’è più gente, perciò scegliamo luoghi meno noti.'),('I posti migliori per l\'alba','L\'alba è ideale per i luoghi che raggiungete prima degli impianti. Il Lago di Braies è magico prima della sua finestra di traffico delle 10 &mdash; immobile come uno specchio e deserto; la strada a pedaggio delle Tre Cime è aperta di notte, così potete salire per la prima luce sulle cime; e creste come il Seceda significano o una salita con la frontale o una notte in rifugio, perché la prima cabina arriva troppo tardi per il colore. Guardate un vero albeggiare in [[s:sunrise-dolomites-elopement|questo elopement all\'alba]].'),('I posti migliori per il tramonto','La sera premia i belvedere in funivia dove prendete l\'ultima cabina in discesa &mdash; o, meglio, dormite in cima. La terrazza del Sass Pordoi, il Lagazuoi con il suo rifugio a strapiombo, i prati dell\'Alpe di Siusi e la Nordkette sopra Innsbruck si accendono nell\'ora d\'oro e restano quieti quando i gitanti se ne vanno. Controllate sempre l\'orario dell\'ultima discesa; dove non c\'è, prenotiamo il rifugio. Di più nei [[g:most-beautiful-dolomites-spots|luoghi più belli]], e una calda sera tirolese in [[s:sunset-elopement-tyrol|questo elopement al tramonto]].')]},
 'elopement-things-nobody-tells-you':{'title':'Ciò che nessuno vi dice sull’elopement','excerpt':'I piccoli dettagli che fanno la differenza &mdash; non dimenticateli.','intro':'Le grandi decisioni sono la parte facile. Sono i piccoli dettagli, poco glamour, a rendere perfetta in silenzio una giornata in montagna &mdash; quelli che nessuna checklist cita. Ecco quelli imparati sulla nostra pelle.','sec':[('Il comfort batte tutto','Portate un secondo paio di scarpe per il cammino, scaldamani, acqua e uno spuntino. Freddo, vesciche o fame si vedono sempre nelle foto &mdash; e nel modo in cui vivete la giornata.'),('Proteggere il momento','Scrivete le promesse in anticipo e portatene una copia stampata &mdash; gli schermi muoiono al freddo. Non dite a nessuno il punto esatto, silenziate i telefoni e lasciate margine perché nulla sembri di fretta.'),('Le cose pratiche che nessuno dice','Portate un po\' di contanti: alcune strade a pedaggio e parcheggi &mdash; la strada delle Tre Cime, il parcheggio di Braies &mdash; sono più comodi in contanti, e a volte anche le cucine dei rifugi. Controllate l\'ultima discesa della funivia prima di puntare sul tramonto, ricordate che Braies chiude al traffico dalle 10 circa in estate, e mettete in valigia uno strato caldo anche ad agosto &mdash; una vetta all\'alba è fredda. E non temete un cielo grigio: la pioggia può essere la cosa migliore, come mostra [[s:rainy-lago-di-braies-pizza-elopement|questo mattino di pioggia a Braies]].'),('Le clausole che vi fanno risparmiare','Poche decisioni anticipate riducono i costi. Prenotate il rifugio e, se vi sposate legalmente in Austria, l\'ufficiale di stato civile con mesi di anticipo &mdash; entrambi sono limitati in estate. La bassa stagione (fine maggio, ottobre) è più economica, tranquilla e spesso più bella, con larici dorati e cime imbiancate. E raramente servono strada a pedaggio e funivia lo stesso giorno &mdash; sceglierne una mantiene semplici budget e programma. Mappiamo tutto in [[g:how-to-plan-your-elopement|come pianificare il vostro elopement]].')]},
}
IT_EX={
 'dolomites-elopement-guide':{'facts':['Giu&ndash;Set','Facile&ndash;Impegnativo','Venezia / Innsbruck &middot; 2&ndash;3 h'],'sec4':('Alba o tramonto?','L’alba significa solitudine e luce morbida con una partenza prima dell’alba; il tramonto è più comodo ma più affollato. Vi aiutiamo a scegliere ciò che fa per voi.'),'tips':['Prenotate presto i rifugi per accedere all’alba.','I larici brillano di più a fine settembre.','Tenete una data flessibile in base al meteo.']},
 'elope-in-austria':{'facts':['Mag&ndash;Ott','Facile&ndash;Moderato','Aeroporto di Innsbruck'],'sec4':('Cerimonia simbolica o legale?','Sposatevi ufficialmente a casa e celebrate una cerimonia simbolica in montagna, oppure completate il matrimonio legale in Austria &mdash; entrambe le opzioni funzionano splendidamente.'),'tips':['L’aeroporto di Innsbruck accorcia il viaggio.','Gli appuntamenti in municipio si riempiono in estate.','Portate abiti a strati &mdash; il meteo di montagna cambia in fretta.']},
 'best-alps-elopement-locations':{'facts':['Dolomiti e Tirolo','Escursione o funivia','Alba'],'sec4':('Quanto camminerete?','Da passeggiate di cinque minuti a vette di un’intera giornata &mdash; adattiamo lo sforzo al vostro comfort, alla forma fisica e alle calzature.'),'tips':['Le funivie regalano grandi panorami con poco sforzo.','I laghi sono più calmi alla prima luce.','Chiedeteci dei luoghi senza permesso.']},
 'how-to-plan-your-elopement':{'facts':['3&ndash;9 mesi','0&ndash;20','Foto &middot; Film &middot; Pianificazione'],'sec4':('Con quanto anticipo prenotare','Le date estive più richieste si riempiono con 6&ndash;12 mesi di anticipo; la bassa stagione è spesso possibile con meno preavviso.'),'tips':['Decidete la sensazione prima del luogo.','Inserite un giorno di margine per il meteo.','Lasciate a noi permessi e fornitori.']},
 'most-beautiful-dolomites-spots':{'facts':['Dolomiti','Funivia o escursione','Alba'],'sec4':('Come scegliere il luogo','Scegliamo il posto in base alla vostra forma, alla stagione e all’atmosfera che desiderate &mdash; calma sul lago, spettacolo sulla cresta o un prato tranquillo.'),'tips':['Andate alla prima luce per evitare la folla.','I laghi smeraldo brillano di più al mattino.','Chiedeteci dei luoghi senza permesso.']},
 'helicopter-elopement-dolomites-guide':{'facts':['In elicottero','Giu&ndash;Set','Volo &asymp; €2.500+'],'sec4':('Cosa può andare storto','Solo il meteo. Se la montagna è chiusa, spostiamo il volo o passiamo a una splendida location a terra &mdash; non perdete mai la giornata.'),'tips':['Prenotate la finestra meteo più ampia possibile.','Portate strati &mdash; in vetta fa freddo.','Tenete il gruppo piccolo per il volo.']},
 'mountain-proposal-guide':{'facts':['Tutto l’anno','Alba','2&ndash;8 settimane'],'sec4':('E dopo il sì?','Continuiamo a fotografare per un servizio di coppia rilassato, poi vi inviamo qualche immagine lo stesso giorno da condividere con la famiglia.'),'tips':['Scegliete un punto con un motivo naturale per fermarsi.','Tenete l’anello al sicuro durante il cammino.','Diteci il segnale così siamo pronti.']},
 'sunrise-or-sunset-elopement':{'facts':['Ora d’oro','Giu&ndash;Ott','Facile&ndash;Moderato'],'sec4':('Il nostro parere sincero','Se reggete la sveglia presto, l’alba vince quasi sempre &mdash; la luce e la solitudine ne valgono la pena. Il tramonto è la scelta rilassata e sicura.'),'tips':['Alba: esplorate il sentiero il giorno prima.','Tramonto: partite prima di quanto pensiate.','In ogni caso: restate per l’ora blu.']},
 'elopement-things-nobody-tells-you':{'facts':['Pianificate presto','0&ndash;20','Promesse &middot; strati &middot; snack'],'sec4':('L’unica cosa da ricordare','È la vostra giornata, non un servizio fotografico. Le immagini migliori nascono quando dimenticate che ci siamo e state semplicemente insieme &mdash; il resto lo pianifichiamo intorno a questo.'),'tips':['Stampate le promesse &mdash; gli schermi falliscono al freddo.','Portate snack, acqua e strati caldi.','Lasciate margine perché nulla sia di fretta.']},
}
# (Italian is merged at the bottom, after TITLES/DESC are defined)

# Home is reachable via the logo, so no "Welcome" link. Contact stays here for the mobile menu
# (the header CTA button is hidden on mobile) but is hidden on desktop via .nav-contact.
NAVKEYS=[('how-to-elope-in-the-europe-mountains/','howto','howto'),
         ('stories-elopement-mountain/','stories','stories'),('our-packages/','packages','packages'),
         ('our-team/','team','team'),('get-in-touch/','contact','contact')]

# ---- Header CTA label (Fix 3) ----
CTA_CONTACT={'en':'Contact','de':'Kontakt','es':'Contacto','it':'Contatto'}

# ---- Structured data / canonical helpers (Fix 4/5) ----
ORG_ID=DOMAIN+'/#organization'
BREADCRUMB_SEG={'how-to-elope-in-the-europe-mountains':'howto','stories-elopement-mountain':'stories',
 'our-packages':'packages','our-team':'team','get-in-touch':'contact'}

def _plain(s):  # strip tags + decode entities for JSON-LD text
    return _html.unescape(re.sub(r'<[^>]+>','',str(s))).strip()

def _crumb_leaf(title):  # page title without the " — Mountain Elopement" / " | …" suffix
    return re.split(r'\s+(?:—|\|)\s+',_plain(title))[0]

def org_ld():
    return {"@context":"https://schema.org","@type":"Organization","@id":ORG_ID,
        "name":"Mountain Elopement","url":DOMAIN+'/',
        "parentOrganization":{"@type":"Organization","name":"Blitzkneisser"},
        "email":"foto@blitzkneisser.com","telephone":"+43 664 39 18 228",
        "address":{"@type":"PostalAddress","streetAddress":"Rohracker 6","postalCode":"6092",
            "addressLocality":"Birgitz","addressCountry":"AT"},
        "sameAs":["https://www.instagram.com/mountainelopement/"]}

def _seg_name(seg,lang):
    if seg in BREADCRUMB_SEG: return _plain(T['nav'][BREADCRUMB_SEG[seg]][lang])
    return seg.replace('-',' ').title()

def breadcrumb_ld(lang,rel,title):
    items=[{"@type":"ListItem","position":1,"name":_plain(T['nav']['welcome'][lang]),"item":f'{DOMAIN}/{lbase(lang)}'}]
    segs=[s for s in rel.split('/') if s]; cum=''
    for i,seg in enumerate(segs):
        cum+=seg+'/'
        name=_crumb_leaf(title) if i==len(segs)-1 else _seg_name(seg,lang)
        items.append({"@type":"ListItem","position":i+2,"name":name,"item":f'{DOMAIN}/{lbase(lang)}{cum}'})
    return {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":items}

def _ld_script(obj):
    return f'<script type="application/ld+json">{json.dumps(obj,ensure_ascii=False,separators=(",",":"))}</script>'

def head(lang, rel, title, desc, ld_extra=None, noindex=False):
    P=prefix(lang,rel)
    alts=''
    for L in LANGS:
        href=f'{DOMAIN}/{lbase(L)}{rel}'
        alts+=f'<link rel="alternate" hreflang="{HREFLANG[L]}" href="{href}">'
    alts+=f'<link rel="alternate" hreflang="x-default" href="{DOMAIN}/{rel}">'
    canonical=f'{DOMAIN}/{lbase(lang)}{rel}'   # self-referential, absolute https, trailing slash, no index.html
    fav=f'<link rel="icon" type="image/png" href="{P}favicon.png"><link rel="apple-touch-icon" href="{P}apple-touch-icon.png">'
    if noindex:  # thank-you page: keep it out of the index, no canonical/structured data
        can='<meta name="robots" content="noindex">'
        ld=''
    else:
        can=f'<link rel="canonical" href="{canonical}">'
        blocks=[org_ld()]
        if [s for s in rel.split('/') if s]: blocks.append(breadcrumb_ld(lang,rel,title))
        if ld_extra: blocks.append(ld_extra)
        ld=''.join(_ld_script(b) for b in blocks)
    return ('<!DOCTYPE html><html lang="'+lang+'"><head><meta charset="UTF-8">'
        '<meta name="viewport" content="width=device-width, initial-scale=1">'
        f'<title>{title}</title><meta name="description" content="{desc}">'
        f'{can}{alts}{fav}{GTM_HEAD}{FONTS}<link rel="stylesheet" href="{P}css/style.css">{ld}</head><body>{GTM_BODY}')

def nav(lang, rel, active, booking=False):
    P=prefix(lang,rel)
    links=''
    for slug,key,akey in NAVKEYS:
        classes=(['active'] if akey==active else [])+(['nav-contact'] if akey=='contact' else [])
        cls=f' class="{" ".join(classes)}"' if classes else ''
        links+=f'<a href="{u(P,lang,slug)}"{cls}>{T["nav"][key][lang]}</a>'
    def langs_block(cls):
        s=f'<div class="{cls}">'
        for i,L in enumerate(LANGS):
            a=' class="active"' if L==lang else ''
            s+=f'<a href="{P}{lbase(L)}{rel}index.html"{a}>{LNAME[L]}</a>'
            if i<len(LANGS)-1: s+='<span class="sep">/</span>'
        return s+'</div>'
    langsw=langs_block('langs')                 # bar (desktop)
    langs_menu=langs_block('langs langs-in-menu')  # inside dropdown (mobile)
    strip=''
    if booking:
        strip=(f'<div class="booking-strip">{t(lang,"booking")} '
               f'<a href="{u(P,lang,"get-in-touch/")}">{t(lang,"booking_link")}</a></div>')
    return (strip+'<header class="masthead"><div class="bar">'
        f'<a class="brand" href="{u(P,lang,"")}"><img class="brand-mark" src="{P}img/logo/mark-dark.png" alt="Mountain Elopement logo"><span class="brand-word">Mountain Elopement</span></a>'
        f'<nav id="nav">{links}{langs_menu}</nav>'
        f'<a class="nav-cta" href="{u(P,lang,"get-in-touch/")}">{CTA_CONTACT[lang]}</a>'
        f'{langsw}'
        '<button class="menu-btn" id="mb" aria-label="Menu">&#9776;</button></div></header>')

def team_section(lang,P):
    def card(role,name,linklabel,url,desc):
        link=(f'<a class="arrow-link" href="{url}" target="_blank" rel="noopener">{linklabel} &rarr;</a>') if url else ''
        return ('<div class="team-card reveal"><div class="role">'+role+'</div><h3>'+name+'</h3><p>'+desc+'</p>'+link+'</div>')
    return ('<section class="partners"><div class="wrap"><div class="section-head reveal">'
        f'<div class="kicker" data-n="{t(lang,"tm_kick")}">{t(lang,"tm_over")}<span class="line"></span></div>'
        f'<h2>{t(lang,"tm_h")}</h2></div><div class="team-grid">'
        +card(t(lang,'tm_r1'),NAME_PLAN,P_PLAN[0],P_PLAN[1],t(lang,'tm_d1'))
        +card(t(lang,'tm_rp'),NAME_PHOTO,'Blitzkneisser','https://blitzkneisser.com',t(lang,'tm_dp'))
        +'</div></div></section>')

def footer(lang,rel):
    P=prefix(lang,rel)
    return ('<footer><div class="wrap"><div class="cols">'
      f'<div><div class="fbrand"><img src="{P}img/logo/mark-light.png" alt="Mountain Elopement logo"><span class="fword">Mountain Elopement</span></div>'
      f'<p>{t(lang,"f_tag")}</p></div>'
      f'<div><h5>{t(lang,"f_explore")}</h5><ul>'
      f'<li><a href="{u(P,lang,"how-to-elope-in-the-europe-mountains/")}">{T["nav"]["howto"][lang]}</a></li>'
      f'<li><a href="{u(P,lang,"stories-elopement-mountain/")}">{T["nav"]["stories"][lang]}</a></li>'
      f'<li><a href="{u(P,lang,"our-packages/")}">{T["nav"]["packages"][lang]}</a></li>'
      f'<li><a href="{u(P,lang,"get-in-touch/")}">{T["nav"]["contact"][lang]}</a></li></ul></div>'
      f'<div><h5>{t(lang,"f_team")}</h5><ul>'
      f'<li><a href="https://blitzkneisser.com" target="_blank" rel="noopener">{t(lang,"f_role_photo")} &middot; Blitzkneisser</a></li>'
      f'<li><a href="{P_PLAN[1]}" target="_blank" rel="noopener">{t(lang,"f_role_plan")} &middot; Dolomites Wedding Planner</a></li>'
      '<li><a href="https://www.instagram.com/mountainelopement/" target="_blank" rel="noopener">Instagram</a></li></ul></div></div>'
      f'<div class="fine"><span>&copy; 2026 mountain-elopement by blitzkneisser.com</span>'
      f'<span><a href="{u(P,lang,"imprint/")}">{t(lang,"f_imprint")}</a> &middot; <a href="{u(P,lang,"privacy-policy/")}">{t(lang,"f_privacy")}</a></span></div></div></footer>')

def scripts(P,extra=''): return f'<script src="{P}js/site.js"></script>{extra}</body></html>'

def write(lang,rel,html):
    path=lbase(lang)+rel+'index.html'
    full=os.path.join(ROOT,path); os.makedirs(os.path.dirname(full),exist_ok=True)
    open(full,'w').write(html)

def story_card(lang,P,s,big=False):
    num,slug,img,cats,titles=s
    tags=' &mdash; '.join(catname(c,lang) for c in cats[:2])
    cls='st big' if big else 'st'
    return (f'<a class="{cls} reveal" href="{u(P,lang,"portfolio-item/"+slug+"/")}">'
        f'<div class="imgwrap"><img src="{P}img/stories/{img}.webp" alt="{titles[lang]}"></div>'
        f'<div class="no">N&deg;{num:02d}</div><h3>{titles[lang]}</h3><div class="tags">{tags}</div></a>')

LB_JS=("<script>var imgs=[].slice.call(document.querySelectorAll('.gallery img'));"
 "var srcs=imgs.map(function(x){return x.getAttribute('src');});var N=srcs.length;"
 "var lb=document.getElementById('lb'),lbimg=document.getElementById('lbimg'),cur=0;"
 "function open(i){cur=i;lbimg.src=srcs[i];lb.classList.add('open');}function close(){lb.classList.remove('open');}"
 "imgs.forEach(function(im,i){im.addEventListener('click',function(){open(i);});});"
 "document.getElementById('lbx').onclick=close;lb.addEventListener('click',function(e){if(e.target===lb)close();});"
 "document.getElementById('lbn').onclick=function(e){e.stopPropagation();open((cur+1)%N);};"
 "document.getElementById('lbp').onclick=function(e){e.stopPropagation();open((cur-1+N)%N);};"
 "addEventListener('keydown',function(e){if(!lb.classList.contains('open'))return;"
 "if(e.key==='Escape')close();if(e.key==='ArrowRight')open((cur+1)%N);if(e.key==='ArrowLeft')open((cur-1+N)%N);});</script>")

MAX_GALLERY=40   # never show more than this many photos per story

def _gallery_files(slug):
    d=os.path.join(ROOT,'img','gallery',slug)
    return [f for f in sorted(os.listdir(d)) if f.lower().endswith('.webp')] if os.path.isdir(d) else []

def _render_gallery(srcs,alt,quote='',full=False):
    n=len(srcs)
    wide=({0} | {i for i in range(5,n,5)}) if full else set()   # full-width breakouts only in feature mode
    qpos=max(2,round(n*0.4)) if (quote and n>=6) else -1  # pull-quote ~40% in
    out=['<div class="gallery">']
    for i,src in enumerate(srcs):
        if i==qpos:
            out.append(f'<figure class="eq"><blockquote>{quote}</blockquote></figure>')
        cls=' class="gfull"' if i in wide else ''
        out.append(f'<img{cls} src="{src}" loading="lazy" alt="{alt}">')
    out.append('</div>')
    return ''.join(out)

def gallery_html(lang,P,slug,alt,quote=''):
    files=_gallery_files(slug)
    if files:
        srcs=[f'{P}img/gallery/{slug}/{fn}' for fn in files[:MAX_GALLERY]]
    else:  # fallback to shared placeholder set
        srcs=[f'{P}img/gallery/g{i:02d}.webp' for i in range(1,13)]
    return _render_gallery(srcs,alt,quote)

TITLES={  # <title> per page
 'home':{'en':'Mountain Elopement | Intimate Weddings & Adventure Elopements','de':'Mountain Elopement — Wo Abenteuer auf Romantik trifft','es':'Mountain Elopement — Donde la aventura se une al romance'},
 'howto':{'en':'How to Elope in Europe | Mountain & Lake Elopement','de':'Elopement in den europäischen Bergen — Mountain Elopement','es':'Cómo fugarse en las montañas de Europa — Mountain Elopement'},
 'stories':{'en':'Stories — Mountain Elopement','de':'Stories — Mountain Elopement','es':'Historias — Mountain Elopement'},
 'packages':{'en':'Price List — Mountain Elopement','de':'Preise — Mountain Elopement','es':'Precios — Mountain Elopement'},
 'team':{'en':'Our Team & Partners — Mountain Elopement','de':'Unser Team & Partner — Mountain Elopement','es':'Nuestro equipo y socios — Mountain Elopement'},
 'contact':{'en':'Contact — Mountain Elopement','de':'Kontakt — Mountain Elopement','es':'Contacto — Mountain Elopement'},
 'thankyou':{'en':'Thank You for Your Inquiry — Mountain Elopement','de':'Danke für eure Anfrage — Mountain Elopement','es':'Gracias por vuestra consulta — Mountain Elopement'},
}
DESC={
 'home':{'en':'Plan your unforgettable Mountain Elopement. We create intimate weddings with breathtaking locations, photography, film & full planning across Europe.','de':'Editorial-Elopement-Fotografie & Planung in den Dolomiten/Alpen.','es':'Fotografía y planificación editorial de elopements en los Dolomitas y los Alpes.'},
 'howto':{'en':'A practical guide to eloping in the European mountains: where to go, what it costs, legal paperwork, and how to plan a day that feels like yours.','de':'Ein Leitfaden für euer Elopement in den Dolomiten/Alpen.','es':'Una guía para fugarse en los Dolomitas y los Alpes.'},
 'stories':{'en':'Mountain elopement stories from the Dolomites and the Alps.','de':'Berg-Elopement-Stories aus den Dolomiten/Alpen.','es':'Historias de elopement de montaña en los Dolomitas y los Alpes.'},
 'packages':{'en':'Elopement packages: photography, planning, film, flowers and make-up.','de':'Elopement-Pakete: Fotografie, Planung, Film, Blumen und Make-up.','es':'Paquetes de elopement: fotografía, planificación, film, flores y maquillaje.'},
 'team':{'en':'The team behind your elopement — photography, planning, film and make-up.','de':'Das Team hinter eurem Elopement — Fotografie, Planung, Film und Make-up.','es':'El equipo detrás de vuestro elopement — fotografía, planificación, film y maquillaje.'},
 'contact':{'en':'Tell us your story. Elopement photography & planning in the Dolomites and the Alps.','de':'Erzählt uns eure Geschichte. Elopement-Fotografie & Planung in den Dolomiten/Alpen.','es':'Contadnos vuestra historia. Fotografía y planificación de elopements en los Dolomitas y los Alpes.'},
 'thankyou':{'en':'Thank you — we\u2019ve received your enquiry.','de':'Danke — wir haben eure Anfrage erhalten.','es':'Gracias — hemos recibido vuestra consulta.'},
}

def build_home(lang):
    rel=''; P=prefix(lang,rel)
    body=(nav(lang,rel,'home',booking=True)+
      f'<section class="hero" style="padding:0"><div class="bg" style="background-image:url(\'{P}img/hero/hero1.webp\')"></div>'
      '<div class="content"><div class="wide"><div><div class="kicker" data-n="Issue N&deg;1"><span class="line"></span></div>'
      f'<h1 class="hero-brand">Mountain Elopement</h1><h2 class="hero-sub">{t(lang,"h_h1").replace("<br>"," ")}</h2></div><div class="side"><p>{t(lang,"h_sub")}</p>'
      f'<a href="{u(P,lang,"get-in-touch/")}" class="btn light">{t(lang,"h_btn")}</a></div></div></div></section>'
      '<section><div class="wrap feature"><div class="body reveal">'
      f'<div class="kicker" data-n="01">{t(lang,"mission_k")}<span class="line"></span></div><h2>{t(lang,"mission_h")}</h2>'
      f'<p class="lead">{t(lang,"mission_lead")}</p><p class="dropcap">{t(lang,"mission_p1")}</p><p>{t(lang,"mission_p2")}</p>'
      f'<a href="{u(P,lang,"how-to-elope-in-the-europe-mountains/")}" class="arrow-link">{t(lang,"mission_link")}</a></div>'
      f'<div class="media reveal"><img src="{P}img/hero/hero2.webp" alt="Wedding ceremony on the Seceda ridge in the Dolomites"><div class="caption">{t(lang,"cap_seceda")}</div></div></div></section>'
      '<hr class="hr"><section><div class="wrap"><div class="section-head reveal">'
      f'<div class="kicker" data-n="{t(lang,"diff_k")}"><span class="line"></span></div><h2>{t(lang,"diff_h")}</h2></div>'
      '<div class="pillars reveal">'
      f'<div class="pillar"><h3>{t(lang,"diff1_h")}</h3><p>{t(lang,"diff1_p")}</p></div>'
      f'<div class="pillar"><h3>{t(lang,"diff2_h")}</h3><p>{t(lang,"diff2_p")}</p></div>'
      f'<div class="pillar"><h3>{t(lang,"diff3_h")}</h3><p>{t(lang,"diff3_p")}</p></div>'
      f'<div class="pillar"><h3>{t(lang,"diff4_h")}</h3><p>{t(lang,"diff4_p")}</p></div></div>'
      '</div></section>'
      '<hr class="hr"><section><div class="wrap"><div class="section-head reveal">'
      f'<div class="kicker" data-n="02">{t(lang,"sel_k")}<span class="line"></span></div><h2>{t(lang,"sel_h")}</h2></div><div class="story-grid">'
      +story_card(lang,P,STORIES[0],big=True)+story_card(lang,P,STORIES[7],big=True)
      +story_card(lang,P,STORIES[3])+story_card(lang,P,STORIES[4])+story_card(lang,P,STORIES[5])
      +f'</div><div style="margin-top:44px" class="reveal"><a href="{u(P,lang,"stories-elopement-mountain/")}" class="btn">{t(lang,"view_all")}</a></div></div></section>'
      '<section style="padding-top:0"><div class="wrap"><div class="figures reveal">'
      f'<div class="f"><div class="num" data-to="125">0</div><div class="lbl">{t(lang,"fig1")}</div></div>'
      f'<div class="f"><div class="num" data-to="253">0</div><div class="lbl">{t(lang,"fig2")}</div></div>'
      f'<div class="f"><div class="num" data-to="2430">0</div><div class="lbl">{t(lang,"fig3")}</div></div>'
      f'<div class="f"><div class="num" data-to="302">0</div><div class="lbl">{t(lang,"fig4")}</div></div></div></div></section>'
      +team_section(lang,P)+
      '<section class="band"><div class="wrap quote reveal">'
      f'<div class="kicker" data-n="03">{t(lang,"kw_k")}<span class="line"></span></div>'
      f'<p style="margin-top:26px">{t(lang,"kw_q")}</p><div class="who">{t(lang,"kw_who")}</div></div></section>'
      '<section class="awards-section"><div class="wrap"><div class="section-head reveal">'
      f'<div class="kicker" data-n="04">{t(lang,"aw_k")}<span class="line"></span></div><h2>{t(lang,"aw_h")}</h2></div>'
      f'<p class="lead reveal" style="max-width:660px">{t(lang,"aw_lead")}</p>'
      '<div class="awards-row reveal">'
      f'<a class="award-item" href="https://wayupnorth.co/2024-wun-awards-photo-contest-winners/" target="_blank" rel="noopener">'
      f'<img class="award-logo" src="{P}img/awards/way-up-north-awards-2024-winner-best-epic-portrait-400.png" alt="Way Up North Awards 2024 &ndash; Winner, Best Epic Portrait" width="400" height="400" loading="lazy" style="height:62px">'
      f'<span class="award-sub">{t(lang,"aw_wun")}</span></a>'
      f'<a class="award-item" href="https://junebugweddings.com/best-wedding-photographers/Austria-photography/" target="_blank" rel="noopener">'
      f'<img class="award-logo" src="{P}img/awards/junebug.webp" alt="Featured on Junebug Weddings" width="300" height="300" loading="lazy" style="height:76px">'
      f'<span class="award-sub">{t(lang,"aw_jb")}</span></a>'
      f'<a class="award-item" href="https://www.fearlessphotographers.com/photographer/7033/andreas-kiss" target="_blank" rel="noopener">'
      f'<img class="award-logo" src="{P}img/awards/fearless.png" alt="Fearless Photographers &ndash; member" width="150" height="150" loading="lazy" style="height:56px">'
      f'<span class="award-sub">{t(lang,"aw_fl")}</span></a>'
      f'<a class="award-item" href="https://rangefinderonline.com/news-features/photo-of-the-day/ankle-deep-in-beauty/" target="_blank" rel="noopener">'
      f'<img class="award-logo" src="{P}img/badges/rangefinder.png" alt="Rangefinder Magazine" width="165" height="165" loading="lazy" style="height:52px">'
      f'<span class="award-sub">{t(lang,"aw_rf")}</span></a>'
      '</div></div></section>'
      '<section class="cta"><div class="wrap row reveal"><div>'
      f'<div class="kicker" data-n="05">{t(lang,"cta_k")}<span class="line"></span></div><h2 style="margin-top:20px">{t(lang,"cta_h")}</h2></div>'
      f'<a href="{u(P,lang,"get-in-touch/")}" class="btn light">{t(lang,"start_planning")}</a></div></section>'
      +footer(lang,rel))
    write(lang,rel,head(lang,rel,TITLES['home'][lang],DESC['home'][lang])+body+scripts(P))

def build_howto(lang):
    rel='how-to-elope-in-the-europe-mountains/'; P=prefix(lang,rel)
    def step(n,tk,pk):
        return ('<div class="reveal" style="grid-column:span 4"><div class="no" style="font-family:var(--sans);color:var(--accent);font-weight:600;letter-spacing:.14em;font-size:12px">STEP '+n+'</div>'
          f'<h3 style="font-family:var(--serif);font-weight:400;font-size:26px;margin:8px 0 10px">{t(lang,tk)}</h3>'
          f'<p style="font-size:17px;color:var(--ink-2)">{t(lang,pk)}</p></div>')
    body=(nav(lang,rel,'howto')+
      f'<section class="page-hero" style="padding:0"><div class="bg" style="background-image:url(\'{P}img/page/howto.webp\')"></div>'
      f'<div class="content"><div class="wrap"><div class="kicker" data-n="{t(lang,"ht_k")}"><span class="line"></span></div><h1>{t(lang,"ht_h1")}</h1>'
      f'<div class="hero-btns"><a class="btn light" href="{u(P,lang,"get-in-touch/")}">{t(lang,"hero_inq")}</a>'
      f'<a class="btn ghost" href="{u(P,lang,"our-packages/")}">{t(lang,"hero_price")}</a></div></div></div></section>'
      '<section><div class="wrap feature"><div class="body reveal">'
      f'<div class="kicker" data-n="01">{t(lang,"ht_s1k")}<span class="line"></span></div><h2>{t(lang,"ht_s1h")}</h2>'
      f'<p class="dropcap">{t(lang,"ht_s1p1")}</p><p>{t(lang,"ht_s1p2")}</p><p>{t(lang,"ht_s1p3")}</p></div>'
      f'<div class="media reveal"><img src="{P}img/stories/s08.webp" alt="Dolomites"><div class="caption">{t(lang,"ht_cap")}</div></div></div></section>'
      '<hr class="hr"><section><div class="wrap"><div class="section-head reveal">'
      f'<div class="kicker" data-n="02">{t(lang,"ht_e_k")}<span class="line"></span></div><h2>{t(lang,"ht_e_h")}</h2></div>'
      '<div class="story-grid" style="align-items:start">'
      +step('01','ht_step1t','ht_step1p')+step('02','ht_step2t','ht_step2p')+step('03','ht_step3t','ht_step3p')+
      '</div></div></section>'
      '<hr class="hr">'
      +guide_hub(lang,P)+
      team_section(lang,P)+
      '<section class="cta"><div class="wrap row reveal"><div>'
      f'<div class="kicker" data-n="{t(lang,"ht_ready")}"><span class="line"></span></div><h2 style="margin-top:20px">{t(lang,"ht_cta_h")}</h2></div>'
      f'<a href="{u(P,lang,"get-in-touch/")}" class="btn light">{t(lang,"get_in_touch")}</a></div></section>'
      +footer(lang,rel))
    write(lang,rel,head(lang,rel,TITLES['howto'][lang],DESC['howto'][lang])+body+scripts(P,GUIDE_JS))

def build_stories(lang):
    rel='stories-elopement-mountain/'; P=prefix(lang,rel)
    cards=story_card(lang,P,STORIES[0],big=True)+story_card(lang,P,STORIES[7],big=True)
    for i,s in enumerate(STORIES):
        if i in (0,7): continue
        cards+=story_card(lang,P,s)
    body=(nav(lang,rel,'stories')+
      f'<div class="page-plain"><div class="wrap"><div class="kicker" data-n="{t(lang,"st_k")}"><span class="line"></span></div>'
      f'<h1>{t(lang,"st_h")}</h1><p class="lead">{t(lang,"st_lead")}</p></div></div>'
      f'<section><div class="wrap"><div class="story-grid">{cards}</div></div></section>'
      '<section class="cta"><div class="wrap row reveal"><div>'
      f'<div class="kicker" data-n="{t(lang,"st_cta_k")}"><span class="line"></span></div><h2 style="margin-top:20px">{t(lang,"st_cta_h")}</h2></div>'
      f'<a href="{u(P,lang,"get-in-touch/")}" class="btn light">{t(lang,"start_planning")}</a></div></section>'
      +footer(lang,rel))
    write(lang,rel,head(lang,rel,TITLES['stories'][lang],DESC['stories'][lang])+body+scripts(P))

def build_categories(lang):
    for slug in CATS:
        rel=f'portfolio-category/{slug}/'; P=prefix(lang,rel)
        subset=[s for s in STORIES if slug in s[3]]
        cards=''.join(story_card(lang,P,s) for s in subset)
        label=catname(slug,lang)
        lead=t(lang,'cat_lead').replace('{x}',label.lower())
        body=(nav(lang,rel,'stories')+
          f'<div class="page-plain"><div class="wrap"><div class="kicker" data-n="{t(lang,"cat_k")}"><span class="line"></span></div>'
          f'<h1>{label}</h1><p class="lead">{lead}</p></div></div>'
          f'<section><div class="wrap"><div class="story-grid">{cards}</div></div></section>'+footer(lang,rel))
        write(lang,rel,head(lang,rel,f'{label} — Mountain Elopement',DESC['stories'][lang])+body+scripts(P))

# Per-story editorial copy (lead + two paragraphs + a pull-quote), truthful to the location
# and the kind of elopement — never invented details about the real couples.
PI_TEXT={
 'a-journey-of-love-and-adventure':{
  'lead':{'en':'Vows on a snow ridge, a helicopter on the glacier and a first run down in gown and black tie &mdash; Sonja and Felix eloped in the winter Dolomites.','de':'Das Ja auf einem Schneegrat, ein Helikopter am Gletscher und die erste Abfahrt in Kleid und Fliege &mdash; Sonja und Felix gaben sich das Ja in den winterlichen Dolomiten.','es':'Votos en una cresta nevada, un helicóptero en el glaciar y un primer descenso en vestido y esmoquin &mdash; Sonja y Felix se fugaron en los Dolomitas invernales.','it':'Le promesse su una cresta innevata, un elicottero sul ghiacciaio e una prima discesa in abito e papillon &mdash; Sonja e Felix si sono sposati nelle Dolomiti d&rsquo;inverno.'},
  'p1':{'en':'They wanted their wedding to feel like the best adventure of their lives, so we took it into the snow. A short flight set them on a high shoulder beneath the Cadini spires, the Seceda ridgeline burning gold behind them. Between the bouquet and the first look under the veil, the whole white amphitheatre of the Dolomites was theirs alone &mdash; no aisle but a windswept ridge, no guests but the peaks.','de':'Sie wollten, dass sich ihre Hochzeit wie das größte Abenteuer ihres Lebens anfühlt &mdash; also gingen wir in den Schnee. Ein kurzer Flug setzte sie auf eine hohe Schulter unter den Cadini-Zinnen ab, der Seceda-Grat glühte golden hinter ihnen. Zwischen Brautstrauß und erstem Blick unter dem Schleier gehörte ihnen das ganze weiße Amphitheater der Dolomiten allein &mdash; kein Mittelgang außer einem windverwehten Grat, keine Gäste außer den Gipfeln.','es':'Querían que su boda se sintiera como la mayor aventura de su vida, así que la llevamos a la nieve. Un breve vuelo los dejó en un alto hombro bajo las agujas de los Cadini, con la cresta del Seceda ardiendo dorada detrás. Entre el ramo y el primer vistazo bajo el velo, todo el anfiteatro blanco de los Dolomitas fue solo suyo &mdash; sin pasillo salvo una cresta batida por el viento, sin invitados salvo las cumbres.','it':'Volevano che le nozze fossero l&rsquo;avventura più bella della loro vita, così le abbiamo portate nella neve. Un breve volo li ha posati su un&rsquo;alta spalla sotto le guglie dei Cadini, con la cresta del Seceda che ardeva d&rsquo;oro dietro di loro. Tra il bouquet e il primo sguardo sotto il velo, tutto il bianco anfiteatro delle Dolomiti è stato solo loro &mdash; nessuna navata se non una cresta spazzata dal vento, nessun invitato se non le cime.'},
  'p2':{'en':'Then came the part they will tell for years: still in gown and black tie, they clipped in and carved the first run down together, veil streaming, snow flying. A winter elopement asks for warm layers, good edges and a flexible eye on the weather &mdash; we handle the flight, the timing and the light, so all you bring is the nerve to ski your own wedding.','de':'Dann kam der Teil, von dem sie noch in Jahren erzählen werden: noch immer in Kleid und Fliege schnallten sie sich an und zogen gemeinsam die erste Abfahrt, der Schleier flatterte, der Schnee stob. Ein Winter-Elopement verlangt warme Schichten, griffige Kanten und ein flexibles Auge fürs Wetter &mdash; wir kümmern uns um Flug, Timing und Licht, ihr bringt nur den Mut mit, eure eigene Hochzeit hinunterzufahren.','es':'Luego llegó lo que contarán durante años: aún en vestido y esmoquin, se ataron las tablas y trazaron juntos el primer descenso, el velo al viento, la nieve volando. Un elopement invernal pide capas de abrigo, buenos cantos y un ojo flexible en el clima &mdash; nosotros nos ocupamos del vuelo, los tiempos y la luz; vosotros solo traéis el valor de esquiar vuestra propia boda.','it':'Poi è arrivata la parte che racconteranno per anni: ancora in abito e papillon, si sono agganciati e hanno tracciato insieme la prima discesa, il velo al vento, la neve che volava. Un elopement invernale chiede strati caldi, lamine buone e un occhio flessibile sul meteo &mdash; pensiamo noi al volo, ai tempi e alla luce; voi portate solo il coraggio di sciare le vostre nozze.'},
  'quote':{'en':'Married on the ridge, and down the mountain before the light was gone.','de':'Am Grat getraut &mdash; und die Abfahrt hinunter, ehe das Licht ging.','es':'Casados en la cresta, y montaña abajo antes de que se fuera la luz.','it':'Sposati sulla cresta, e giù per la montagna prima che sparisse la luce.'}},
 'adventure-helicopter-elopement-dolomites':{
  'lead':{'en':'The Dolomites the way almost no one sees them &mdash; from a summit reached by rotor, not by trail.','de':'Die Dolomiten, wie sie fast niemand sieht &mdash; auf einem Gipfel, den ihr per Rotor erreicht, nicht per Weg.','es':'Los Dolomitas como casi nadie los ve &mdash; en una cumbre a la que se llega en helicóptero, no a pie.','it':'Le Dolomiti come quasi nessuno le vede &mdash; su una vetta raggiunta in elicottero, non a piedi.'},
  'p1':{'en':'A helicopter lifts you over the peaks and sets you down where the crowds can never follow &mdash; a remote ledge of rock and snow, the whole range spread beneath your feet. Minutes earlier you were in the valley; now you have a summit to yourselves.','de':'Ein Helikopter hebt euch über die Gipfel und setzt euch dort ab, wohin keine Menschenmenge folgen kann &mdash; ein einsames Band aus Fels und Schnee, das ganze Massiv zu euren Füßen. Eben noch im Tal, gehört euch jetzt ein Gipfel ganz allein.','es':'Un helicóptero os eleva sobre las cumbres y os deja donde las multitudes no pueden llegar &mdash; un rincón remoto de roca y nieve, con toda la cordillera a vuestros pies. Hace minutos estabais en el valle; ahora la cima es solo vuestra.','it':'Un elicottero vi solleva sopra le cime e vi posa dove la folla non arriva mai &mdash; un lembo remoto di roccia e neve, con l&rsquo;intera catena sotto i piedi. Pochi minuti prima eravate a valle; ora la vetta è tutta vostra.'},
  'p2':{'en':'It is the shortcut to the extraordinary: no multi-day trek, no compromise on the view. We handle the flight, the timing and the light, so all you carry up is each other.','de':'Es ist die Abkürzung zum Außergewöhnlichen: keine Mehrtagestour, kein Kompromiss bei der Aussicht. Wir kümmern uns um Flug, Timing und Licht &mdash; ihr bringt nur einander mit hinauf.','es':'Es el atajo a lo extraordinario: sin travesías de varios días, sin renunciar a las vistas. Nosotros nos ocupamos del vuelo, los tiempos y la luz; vosotros solo lleváis al otro.','it':'È la scorciatoia verso lo straordinario: nessun trekking di più giorni, nessun compromesso sul panorama. Pensiamo noi al volo, ai tempi e alla luce; voi portate soltanto l&rsquo;altro.'},
  'quote':{'en':'Above the clouds, the only witnesses are the peaks.','de':'Über den Wolken sind die Gipfel die einzigen Zeugen.','es':'Sobre las nubes, los únicos testigos son las cumbres.','it':'Sopra le nuvole, gli unici testimoni sono le cime.'}},
 'climbing-wedding':{
  'lead':{'en':'Rope, harness and a ridge for an aisle &mdash; a wedding for two who feel most at home on the rock.','de':'Seil, Gurt und ein Grat als Mittelgang &mdash; eine Hochzeit für zwei, die sich am Fels zu Hause fühlen.','es':'Cuerda, arnés y una cresta por pasillo &mdash; una boda para dos que se sienten en casa en la roca.','it':'Corda, imbrago e una cresta come navata &mdash; un matrimonio per due che sulla roccia si sentono a casa.'},
  'p1':{'en':'For some couples the climb isn&rsquo;t the way to the ceremony &mdash; it is the ceremony. Hands chalked, exposure below, they moved together up the wall and said their vows where the only way down is the way you came.','de':'Für manche Paare ist der Aufstieg nicht der Weg zur Zeremonie &mdash; er ist die Zeremonie. Hände im Chalk, Tiefe unter sich, kletterten sie gemeinsam die Wand hinauf und gaben sich das Ja dort, wo der einzige Weg zurück der Weg hinauf ist.','es':'Para algunas parejas la escalada no es el camino a la ceremonia &mdash; es la ceremonia. Con las manos en magnesio y el vacío debajo, subieron juntos la pared y se dieron el sí donde la única bajada es por donde subiste.','it':'Per alcune coppie la salita non è la via verso la cerimonia &mdash; è la cerimonia. Mani nella magnesite, il vuoto sotto, hanno salito insieme la parete e si sono promessi dove l&rsquo;unica discesa è la via di salita.'},
  'p2':{'en':'Trust is the whole story here &mdash; the same trust a marriage runs on. We shoot light and move with certified guides, so the day is bold but never reckless.','de':'Vertrauen ist hier die ganze Geschichte &mdash; dasselbe Vertrauen, von dem eine Ehe lebt. Wir fotografieren leicht und bewegen uns mit zertifizierten Bergführern: mutig, aber nie leichtsinnig.','es':'La confianza es toda la historia &mdash; la misma sobre la que se sostiene un matrimonio. Trabajamos ligeros y con guías certificados, para que el día sea audaz pero nunca temerario.','it':'La fiducia è tutta la storia &mdash; la stessa su cui si regge un matrimonio. Lavoriamo leggeri e ci muoviamo con guide certificate: audaci, mai imprudenti.'},
  'quote':{'en':'One rope, two people, everything to trust.','de':'Ein Seil, zwei Menschen, alles Vertrauen.','es':'Una cuerda, dos personas, toda la confianza.','it':'Una corda, due persone, tutta la fiducia.'}},
 'couple-shoot-photo':{
  'lead':{'en':'No ceremony, no guest list &mdash; just the two of you and a mountain evening to spend it in.','de':'Keine Zeremonie, keine Gästeliste &mdash; nur ihr beide und ein Bergabend, um ihn zu verbringen.','es':'Sin ceremonia, sin lista de invitados &mdash; solo vosotros dos y una tarde de montaña por delante.','it':'Nessuna cerimonia, nessuna lista di invitati &mdash; solo voi due e una sera di montagna da vivere.'},
  'p1':{'en':'Sometimes you don&rsquo;t need an occasion &mdash; you just want honest pictures of the two of you, somewhere beautiful. We walked out into the hills at the end of the day and let the conversation, and the light, do the rest.','de':'Manchmal braucht es keinen Anlass &mdash; ihr wollt einfach ehrliche Bilder von euch beiden, an einem schönen Ort. Wir gingen am Abend hinaus in die Berge und ließen das Gespräch und das Licht den Rest tun.','es':'A veces no hace falta una ocasión &mdash; solo queréis fotos sinceras de los dos, en un lugar bonito. Salimos a las colinas al caer el día y dejamos que la conversación, y la luz, hicieran el resto.','it':'A volte non serve un&rsquo;occasione &mdash; volete solo foto sincere di voi due, in un posto bello. Siamo usciti tra i monti a fine giornata e abbiamo lasciato che il dialogo, e la luce, facessero il resto.'},
  'p2':{'en':'It&rsquo;s the easiest way to meet a camera before a wedding day &mdash; or simply to mark being in love, right now, in a place you&rsquo;ll want to remember.','de':'Es ist der leichteste Weg, sich vor dem Hochzeitstag an die Kamera zu gewöhnen &mdash; oder einfach das Verliebtsein festzuhalten, genau jetzt, an einem Ort, den ihr in Erinnerung behalten wollt.','es':'Es la forma más fácil de conocer la cámara antes de la boda &mdash; o simplemente de celebrar estar enamorados, ahora mismo, en un lugar que querréis recordar.','it':'È il modo più semplice per prendere confidenza con la macchina prima delle nozze &mdash; o solo per celebrare l&rsquo;amore, ora, in un luogo che vorrete ricordare.'},
  'quote':{'en':'Just the two of you &mdash; that was always enough.','de':'Nur ihr beide &mdash; das war immer genug.','es':'Solo vosotros dos &mdash; siempre fue suficiente.','it':'Solo voi due &mdash; è sempre bastato.'}},
 'crystal-clear-water-elopement':{
  'lead':{'en':'An alpine lake so clear it doubles the sky &mdash; and a promise made at the water&rsquo;s edge.','de':'Ein Bergsee, so klar, dass er den Himmel verdoppelt &mdash; und ein Versprechen am Ufer.','es':'Un lago alpino tan claro que duplica el cielo &mdash; y una promesa a la orilla del agua.','it':'Un lago alpino così limpido da raddoppiare il cielo &mdash; e una promessa in riva all&rsquo;acqua.'},
  'p1':{'en':'High meltwater lakes hold a colour photos struggle to believe &mdash; glassy turquoise over pale stone, mountains standing on their own reflection. This day belonged to that stillness, the pair of them small against all that light.','de':'Hoch gelegene Schmelzwasserseen tragen eine Farbe, die Fotos kaum glauben &mdash; gläsernes Türkis über hellem Stein, Berge auf ihrem eigenen Spiegelbild. Dieser Tag gehörte dieser Stille, die beiden klein vor all dem Licht.','es':'Los lagos de deshielo guardan un color que las fotos apenas creen &mdash; turquesa cristalino sobre piedra clara, montañas de pie sobre su propio reflejo. Este día perteneció a esa quietud, los dos pequeños ante tanta luz.','it':'I laghi d&rsquo;alta quota custodiscono un colore che le foto stentano a credere &mdash; turchese vitreo su pietra chiara, montagne in piedi sul proprio riflesso. Questa giornata è appartenuta a quella quiete, loro due piccoli davanti a tanta luce.'},
  'p2':{'en':'We timed it for calm water and soft sun, when the surface goes to mirror. Bring good shoes and a sense of wonder; the lake supplies the rest.','de':'Wir legten es auf ruhiges Wasser und weiche Sonne, wenn die Oberfläche zum Spiegel wird. Bringt gute Schuhe und Staunen mit &mdash; den Rest liefert der See.','es':'Lo planeamos para agua en calma y sol suave, cuando la superficie se vuelve espejo. Traed buen calzado y algo de asombro; el lago pone lo demás.','it':'Abbiamo scelto acqua calma e sole morbido, quando la superficie diventa specchio. Portate scarpe buone e un po&rsquo; di stupore; al resto pensa il lago.'},
  'quote':{'en':'Still water, and two people sure of each other.','de':'Stilles Wasser und zwei, die sich sicher sind.','es':'Agua quieta y dos personas seguras del otro.','it':'Acqua ferma e due persone sicure l&rsquo;una dell&rsquo;altra.'}},
 'hiking-elopement-lagazuoi-dolomites':{
  'lead':{'en':'A civil ceremony in Selva, a helicopter to a snow-clad Dolomite peak and a ski run down in gown and black tie &mdash; Max and Jelena married in winter Val Gardena.','de':'Eine standesamtliche Trauung in Wolkenstein, ein Helikopter auf einen verschneiten Dolomitengipfel und die Abfahrt in Kleid und Fliege &mdash; Max und Jelena heirateten im winterlichen Gröden.','es':'Una ceremonia civil en Selva, un helicóptero a una cima nevada de los Dolomitas y un descenso esquiando en vestido y esmoquin &mdash; Max y Jelena se casaron en el Val Gardena invernal.','it':'Una cerimonia civile a Selva, un elicottero su una cima innevata delle Dolomiti e una discesa sugli sci in abito e papillon &mdash; Max e Jelena si sono sposati nella Val Gardena d&rsquo;inverno.'},
  'p1':{'en':'Theirs was a real winter wedding, kept small and spent entirely in the snow. They said their legal vows at the registry in Selva di Val Gardena &mdash; red folder, the town&rsquo;s crest, the registrar&rsquo;s tricolour sash &mdash; with only their closest people around them. Then a helicopter lifted the two of them out of the valley and set them on a high, wind-scoured shoulder of the Gröden Dolomites, the peaks standing white against a heavy winter sky.','de':'Es war eine echte Winterhochzeit &mdash; klein gehalten und ganz im Schnee verbracht. Ihr Ja gaben sie sich standesamtlich in Wolkenstein (Selva di Val Gardena) &mdash; rote Mappe, das Wappen des Ortes, die Trikolore-Schärpe des Bürgermeisters &mdash; nur die engsten Menschen um sich. Dann hob ein Helikopter die beiden aus dem Tal und setzte sie auf eine hohe, windgefegte Schulter der Grödner Dolomiten ab, die Gipfel weiß vor schwerem Winterhimmel.','es':'Fue una boda de invierno de verdad &mdash; íntima y pasada entera en la nieve. Dieron el sí legal en el registro de Selva di Val Gardena &mdash; carpeta roja, el escudo del pueblo, la banda tricolor del alcalde &mdash; solo con sus más allegados. Luego un helicóptero los elevó del valle y los dejó en un alto hombro barrido por el viento de los Dolomitas de Gröden, las cumbres blancas ante un cielo cargado de invierno.','it':'È stato un vero matrimonio d&rsquo;inverno &mdash; piccolo e vissuto interamente nella neve. Il sì legale l&rsquo;hanno detto al municipio di Selva di Val Gardena &mdash; cartella rossa, lo stemma del paese, la fascia tricolore del sindaco &mdash; con accanto solo le persone più care. Poi un elicottero li ha sollevati dalla valle e posati su un&rsquo;alta spalla spazzata dal vento delle Dolomiti gardenesi, le cime bianche contro un cielo carico d&rsquo;inverno.'},
  'p2':{'en':'What came next is pure Max and Jelena: still in gown and black tie, they buckled in and rode the piste back down, then met their families for Aperol and a long, sunlit lunch on a mountain-hut terrace, the Sassolungo glowing behind them. A winter day like this asks for warm layers, a helicopter window and a flexible eye on the weather &mdash; we handle the flight, the timing and the light, so you can simply get married and then ski home.','de':'Was dann kam, ist ganz Max und Jelena: noch in Kleid und Fliege schnallten sie sich an und fuhren die Piste hinunter, dann trafen sie ihre Familien zu Aperol und einem langen, sonnigen Mittagessen auf einer Hüttenterrasse, der Langkofel leuchtend im Rücken. So ein Wintertag verlangt warme Schichten, ein Helikopterfenster und ein flexibles Auge fürs Wetter &mdash; wir kümmern uns um Flug, Timing und Licht, ihr heiratet einfach und fahrt dann nach Hause.','es':'Lo que vino después es puro Max y Jelena: aún en vestido y esmoquin, se ataron las tablas y bajaron la pista, y luego se reunieron con sus familias para un Aperol y un largo almuerzo al sol en la terraza de un refugio, con el Sassolungo brillando detrás. Un día así pide capas de abrigo, una ventanilla de helicóptero y un ojo flexible en el clima &mdash; nosotros nos ocupamos del vuelo, los tiempos y la luz; vosotros solo os casáis y luego bajáis esquiando a casa.','it':'Ciò che è venuto dopo è puro Max e Jelena: ancora in abito e papillon, si sono agganciati e hanno sceso la pista, poi hanno raggiunto le famiglie per un Aperol e un lungo pranzo al sole sulla terrazza di un rifugio, con il Sassolungo che brillava alle spalle. Una giornata così chiede strati caldi, un finestrino d&rsquo;elicottero e un occhio flessibile sul meteo &mdash; pensiamo noi al volo, ai tempi e alla luce; voi vi sposate e basta, poi scendete a casa sugli sci.'},
  'quote':{'en':'Legally wed in the valley, airborne by noon, and home down the piste.','de':'Im Tal getraut, mittags in der Luft &mdash; und über die Piste nach Hause.','es':'Casados en el valle, en el aire al mediodía, y a casa por la pista.','it':'Sposati a valle, in volo a mezzogiorno, e a casa lungo la pista.'}},
 'intimate-lake-eibsee-elopement':{
  'lead':{'en':'The Eibsee &mdash; turquoise water and wooded islets at the foot of Germany&rsquo;s highest peak.','de':'Der Eibsee &mdash; türkises Wasser und bewaldete Inseln am Fuß von Deutschlands höchstem Gipfel.','es':'El Eibsee &mdash; agua turquesa e islotes boscosos al pie de la cima más alta de Alemania.','it':'L&rsquo;Eibsee &mdash; acqua turchese e isolotti boscosi ai piedi della vetta più alta della Germania.'},
  'p1':{'en':'Below the Zugspitze lies a lake the colour of sea glass, ringed by pines and threaded with tiny islands. Early in the morning it is almost empty, and the pair had its coves and its light entirely to themselves.','de':'Unter der Zugspitze liegt ein See in der Farbe von Meerglas, gesäumt von Kiefern und durchzogen von winzigen Inseln. Früh am Morgen ist er fast leer &mdash; die beiden hatten seine Buchten und sein Licht ganz für sich.','es':'Bajo el Zugspitze se extiende un lago del color del vidrio marino, rodeado de pinos y salpicado de islas diminutas. Temprano está casi vacío, y la pareja tuvo sus calas y su luz para ella sola.','it':'Sotto lo Zugspitze si distende un lago del colore del vetro di mare, cinto di pini e punteggiato di isolotti. Al mattino presto è quasi deserto, e i due hanno avuto le sue insenature e la sua luce tutte per sé.'},
  'p2':{'en':'Reachable in minutes yet wonderfully quiet, the Eibsee suits couples who want a wild-looking day without a long march to reach it.','de':'In Minuten erreichbar und doch wunderbar still, passt der Eibsee zu Paaren, die einen wild wirkenden Tag wollen &mdash; ohne langen Marsch dorthin.','es':'Accesible en minutos y a la vez maravillosamente tranquilo, el Eibsee va con parejas que quieren un día de aspecto salvaje sin una larga marcha para llegar.','it':'Raggiungibile in pochi minuti eppure meravigliosamente quieto, l&rsquo;Eibsee è ideale per coppie che vogliono una giornata dall&rsquo;aria selvaggia senza una lunga marcia per arrivarci.'},
  'quote':{'en':'Green water, quiet pines, and all the time in the world.','de':'Grünes Wasser, stille Kiefern und alle Zeit der Welt.','es':'Agua verde, pinos en calma y todo el tiempo del mundo.','it':'Acqua verde, pini quieti e tutto il tempo del mondo.'}},
 'lago-di-braies-elopement':{
  'lead':{'en':'Lago di Braies &mdash; emerald water, a wooden boathouse, and the Dolomites rising straight out of the lake.','de':'Pragser Wildsee &mdash; smaragdgrünes Wasser, ein hölzernes Bootshaus und Dolomiten, die direkt aus dem See wachsen.','es':'Lago di Braies &mdash; agua esmeralda, una caseta de madera y los Dolomitas surgiendo del propio lago.','it':'Lago di Braies &mdash; acqua smeraldo, una casetta delle barche in legno e le Dolomiti che salgono dritte dal lago.'},
  'p1':{'en':'They call it the pearl of the Dolomites: a mirror of green water, the old boathouse and its wooden rowboats, the Croda del Becco standing guard at the far end. It is one of the most photographed places in the Alps &mdash; and, at dawn, one of the most peaceful.','de':'Man nennt ihn die Perle der Dolomiten: ein Spiegel aus grünem Wasser, das alte Bootshaus mit seinen Ruderbooten, die Croda del Becco als Wächter am anderen Ende. Einer der meistfotografierten Orte der Alpen &mdash; und im Morgengrauen einer der friedlichsten.','es':'Lo llaman la perla de los Dolomitas: un espejo de agua verde, la vieja caseta con sus barcas de remos, la Croda del Becco vigilando al fondo. Es uno de los lugares más fotografiados de los Alpes &mdash; y, al amanecer, uno de los más serenos.','it':'Lo chiamano la perla delle Dolomiti: uno specchio d&rsquo;acqua verde, l&rsquo;antica casetta con le sue barche a remi, la Croda del Becco a guardia in fondo. È uno dei luoghi più fotografati delle Alpi &mdash; e, all&rsquo;alba, uno dei più sereni.'},
  'p2':{'en':'To have it quiet you go early, before the boats and the buses. We plan around first light, when the water is still and the colour is at its deepest.','de':'Um ihn still zu erleben, kommt man früh &mdash; vor den Booten und den Bussen. Wir planen um das erste Licht, wenn das Wasser ruht und die Farbe am tiefsten ist.','es':'Para tenerlo en calma hay que ir temprano, antes de las barcas y los autobuses. Planificamos en torno a la primera luz, cuando el agua está quieta y el color es más intenso.','it':'Per averlo in pace si va presto, prima delle barche e dei pullman. Pianifichiamo attorno alla prima luce, quando l&rsquo;acqua è ferma e il colore è più profondo.'},
  'quote':{'en':'The pearl of the Dolomites, and a morning all your own.','de':'Die Perle der Dolomiten und ein Morgen ganz für euch.','es':'La perla de los Dolomitas y una mañana solo vuestra.','it':'La perla delle Dolomiti e un mattino tutto vostro.'}},
 'rainy-lago-di-braies-pizza-elopement':{
  'lead':{'en':'Emerald water, wooden rowboats and a passing summer shower &mdash; Sussette and Gabriel eloped at Lago di Braies and baked their own pizza by the lake.','de':'Smaragdgrünes Wasser, hölzerne Ruderboote und ein vorüberziehender Sommerregen &mdash; Sussette und Gabriel gaben sich am Pragser Wildsee das Ja und backten ihre eigene Pizza am See.','es':'Agua esmeralda, barcas de remos de madera y un chubasco de verano de paso &mdash; Sussette y Gabriel se fugaron en el Lago di Braies y hornearon su propia pizza junto al lago.','it':'Acqua smeraldo, barche a remi di legno e un acquazzone estivo di passaggio &mdash; Sussette e Gabriel si sono sposati al Lago di Braies e hanno cotto la loro pizza in riva al lago.'},
  'p1':{'en':'The morning came in grey and wet, cloud sitting low on the Croda del Becco and rain freckling the old wooden jetty. It changed nothing. Under a clear umbrella they read their vows to the sound of the water, exchanged rings among the moored rowboats, and then pushed one out onto the lake &mdash; just the two of them, drifting on that impossible green while the mist moved across the cliffs.','de':'Der Morgen kam grau und nass, Wolken tief an der Croda del Becco, Regen sprenkelte den alten Holzsteg. Es änderte nichts. Unter einem durchsichtigen Schirm lasen sie ihre Versprechen zum Klang des Wassers, tauschten die Ringe zwischen den vertäuten Ruderbooten und stießen dann eines hinaus auf den See &mdash; nur sie beide, treibend auf diesem unmöglichen Grün, während der Nebel über die Felswände zog.','es':'La mañana llegó gris y mojada, la nube posada baja sobre la Croda del Becco y la lluvia salpicando el viejo embarcadero de madera. No cambió nada. Bajo un paraguas transparente leyeron sus votos al son del agua, intercambiaron los anillos entre las barcas amarradas y luego empujaron una hacia el lago &mdash; solos los dos, a la deriva sobre ese verde imposible mientras la niebla recorría los farallones.','it':'Il mattino è arrivato grigio e bagnato, le nuvole basse sulla Croda del Becco e la pioggia a punteggiare il vecchio pontile di legno. Non ha cambiato nulla. Sotto un ombrello trasparente hanno letto le promesse al suono dell&rsquo;acqua, si sono scambiati gli anelli tra le barche ormeggiate e poi ne hanno spinta una sul lago &mdash; loro due soli, alla deriva su quel verde impossibile mentre la nebbia scivolava sulle pareti.'},
  'p2':{'en':'When the shower grew heavier we ducked under the boathouse roof and lit the pizza oven &mdash; and that became the day. Dough tossed, a wood-fired margherita slid onto the peel, both of them laughing over the flames while Braies steamed behind them. The rain passed, as it always does, and they finished with a spray of champagne in an alpine meadow. It is the kind of day rain can&rsquo;t spoil &mdash; and we plan it so a grey sky is never a problem, only a plot twist.','de':'Als der Schauer stärker wurde, schlüpften wir unter das Dach des Bootshauses und heizten den Pizzaofen an &mdash; und genau das wurde der Tag. Teig geworfen, eine Margherita aus dem Holzofen auf die Schaufel geschoben, beide lachend über den Flammen, während Braies hinter ihnen dampfte. Der Regen zog vorüber, wie immer, und sie ließen den Tag mit einer Ladung Champagner auf einer Almwiese ausklingen. Es ist die Art Tag, die Regen nicht verderben kann &mdash; und wir planen ihn so, dass ein grauer Himmel nie ein Problem ist, nur eine Wendung.','es':'Cuando el chubasco arreció nos metimos bajo el tejado de la caseta y encendimos el horno de pizza &mdash; y eso se convirtió en el día. Masa al aire, una margarita al horno de leña sobre la pala, los dos riéndose sobre las llamas mientras Braies humeaba detrás. La lluvia pasó, como siempre, y remataron con un chorro de champán en un prado alpino. Es la clase de día que la lluvia no puede estropear &mdash; y lo planeamos para que un cielo gris nunca sea un problema, solo un giro de guion.','it':'Quando l&rsquo;acquazzone si è fatto più forte ci siamo infilati sotto il tetto della casetta e abbiamo acceso il forno della pizza &mdash; ed è diventato quello il giorno. Impasto in aria, una margherita nel forno a legna sulla pala, entrambi a ridere sopra le fiamme mentre Braies fumava dietro di loro. La pioggia è passata, come sempre, e hanno chiuso con una spruzzata di champagne in un prato alpino. È il tipo di giornata che la pioggia non può rovinare &mdash; e la pianifichiamo perché un cielo grigio non sia mai un problema, solo un colpo di scena.'},
  'quote':{'en':'The rain came, the pizza rose, and nobody wanted to be anywhere else.','de':'Der Regen kam, die Pizza ging auf &mdash; und niemand wollte woanders sein.','es':'Llegó la lluvia, subió la pizza, y nadie quería estar en otro sitio.','it':'È arrivata la pioggia, è lievitata la pizza, e nessuno voleva essere altrove.'}},
 'lake-elopement-tyrol-mountains':{
  'lead':{'en':'A quiet Tyrolean lake in the high country &mdash; alpine water, close to Innsbruck, far from everything.','de':'Ein stiller Tiroler Bergsee im Hochland &mdash; alpines Wasser, nah an Innsbruck, fern von allem.','es':'Un lago tirolés tranquilo en la alta montaña &mdash; agua alpina, cerca de Innsbruck, lejos de todo.','it':'Un quieto lago tirolese d&rsquo;alta quota &mdash; acqua alpina, vicino a Innsbruck, lontano da tutto.'},
  'p1':{'en':'Tyrol keeps its lakes tucked into the folds of the mountains, minutes from the valley yet a world away. This one gave the couple cold clear water, a rim of peaks, and the particular hush that settles over the Alps out of season.','de':'Tirol verbirgt seine Seen in den Falten der Berge &mdash; Minuten vom Tal entfernt und doch eine Welt für sich. Dieser schenkte dem Paar kaltes klares Wasser, einen Kranz aus Gipfeln und jene besondere Stille, die sich außerhalb der Saison über die Alpen legt.','es':'El Tirol guarda sus lagos en los pliegues de las montañas, a minutos del valle y a la vez en otro mundo. Este dio a la pareja agua fría y clara, un anillo de cumbres y ese silencio particular que cubre los Alpes fuera de temporada.','it':'Il Tirolo custodisce i suoi laghi nelle pieghe dei monti, a pochi minuti dalla valle eppure in un altro mondo. Questo ha regalato alla coppia acqua fredda e limpida, una corona di cime e quel silenzio particolare che scende sulle Alpi fuori stagione.'},
  'p2':{'en':'With Innsbruck airport so near, Tyrol is the easy door into the high Alps &mdash; big scenery without a long journey to find it.','de':'Mit dem Flughafen Innsbruck so nah ist Tirol die bequeme Tür in die Hochalpen &mdash; große Landschaft ohne lange Anreise.','es':'Con el aeropuerto de Innsbruck tan cerca, el Tirol es la puerta fácil a los Alpes altos &mdash; gran paisaje sin un viaje largo.','it':'Con l&rsquo;aeroporto di Innsbruck così vicino, il Tirolo è la porta comoda verso le Alpi alte &mdash; grandi paesaggi senza un lungo viaggio.'},
  'quote':{'en':'High water, thin air, and no one else for miles.','de':'Hohes Wasser, dünne Luft und weit und breit niemand.','es':'Agua de altura, aire fino y nadie en kilómetros.','it':'Acqua d&rsquo;alta quota, aria sottile e nessun altro per chilometri.'}},
 'mountain-elopement-dolomiten':{
  'lead':{'en':'The Dolomites at their most classic &mdash; pale spires, deep valleys, and a day shaped around them.','de':'Die Dolomiten in ihrer klassischsten Form &mdash; helle Zinnen, tiefe Täler und ein Tag, ganz um sie herum gebaut.','es':'Los Dolomitas en su forma más clásica &mdash; agujas pálidas, valles profundos y un día pensado en torno a ellos.','it':'Le Dolomiti nella loro forma più classica &mdash; guglie chiare, valli profonde e una giornata costruita intorno a loro.'},
  'p1':{'en':'The Dolomites don&rsquo;t look like other mountains &mdash; pale limestone towers that blush pink at sunset and glow cold blue at dawn. To elope here is to marry inside a landscape that feels almost invented, jagged and enormous and yours for a morning.','de':'Die Dolomiten sehen aus wie keine anderen Berge &mdash; helle Kalktürme, die bei Sonnenuntergang rosa erglühen und im Morgengrauen kühl blau leuchten. Hier zu heiraten heißt, mitten in einer Landschaft zu heiraten, die fast erfunden wirkt: zackig, gewaltig und für einen Morgen ganz euch.','es':'Los Dolomitas no se parecen a otras montañas &mdash; torres de caliza pálida que se sonrojan de rosa al atardecer y brillan de azul frío al amanecer. Fugarse aquí es casarse dentro de un paisaje que parece casi inventado: dentado, enorme y vuestro por una mañana.','it':'Le Dolomiti non somigliano ad altre montagne &mdash; torri di calcare chiaro che si tingono di rosa al tramonto e brillano d&rsquo;azzurro freddo all&rsquo;alba. Sposarsi qui significa unirsi dentro un paesaggio quasi inventato: frastagliato, immenso e vostro per un mattino.'},
  'p2':{'en':'From roadside meadows to high passes, there is a Dolomite setting for every level of effort. We match the location to how far you want to walk and how wild you want it to feel.','de':'Von Wiesen am Straßenrand bis zu hohen Pässen gibt es für jede Kondition den passenden Dolomiten-Ort. Wir wählen die Location danach, wie weit ihr gehen und wie wild es sich anfühlen soll.','es':'De prados junto a la carretera a puertos de altura, hay un rincón dolomítico para cada nivel de esfuerzo. Elegimos la localización según cuánto queráis caminar y cuán salvaje lo queráis sentir.','it':'Dai prati sul ciglio della strada agli alti passi, c&rsquo;è un angolo dolomitico per ogni livello di fatica. Scegliamo il luogo in base a quanto volete camminare e quanto selvaggio lo volete.'},
  'quote':{'en':'Stone that turns pink at dusk, and a promise beneath it.','de':'Fels, der in der Dämmerung rosa wird &mdash; und ein Versprechen darunter.','es':'Piedra que se vuelve rosa al anochecer, y una promesa debajo.','it':'Pietra che si fa rosa al crepuscolo, e una promessa sotto.'}},
 'mountain-engagement':{
  'lead':{'en':'The question, or the yes still glowing after it &mdash; an engagement morning in the high air.','de':'Die Frage &mdash; oder das noch nachglühende Ja &mdash; ein Verlobungsmorgen in der Höhenluft.','es':'La pregunta, o el sí que aún brilla después &mdash; una mañana de compromiso en el aire de altura.','it':'La domanda, o il sì che ancora risplende dopo &mdash; un mattino di fidanzamento nell&rsquo;aria d&rsquo;alta quota.'},
  'p1':{'en':'An engagement in the mountains is the story before the story &mdash; the giddy, disbelieving hours right after a yes. We climbed a little, laughed a lot, and let the two of them be as new to it as they felt.','de':'Eine Verlobung in den Bergen ist die Geschichte vor der Geschichte &mdash; die schwindligen, ungläubigen Stunden direkt nach einem Ja. Wir stiegen ein Stück hinauf, lachten viel und ließen die beiden so neu darin sein, wie sie sich fühlten.','es':'Un compromiso en la montaña es la historia antes de la historia &mdash; las horas vertiginosas e incrédulas justo después de un sí. Subimos un poco, reímos mucho y dejamos que los dos fueran tan novatos en esto como se sentían.','it':'Un fidanzamento in montagna è la storia prima della storia &mdash; le ore vertiginose e incredule subito dopo un sì. Siamo saliti un poco, abbiamo riso molto e li abbiamo lasciati essere così alle prime armi come si sentivano.'},
  'p2':{'en':'It is also the perfect rehearsal &mdash; a relaxed hour with the camera that makes the wedding day feel like second nature.','de':'Es ist zugleich die perfekte Probe &mdash; eine entspannte Stunde mit der Kamera, die den Hochzeitstag zur Selbstverständlichkeit macht.','es':'Es también el ensayo perfecto &mdash; una hora relajada con la cámara que hace que el día de la boda salga solo.','it':'È anche la prova perfetta &mdash; un&rsquo;ora rilassata con la macchina che rende il giorno delle nozze naturale.'},
  'quote':{'en':'A yes said out loud, with only the mountains watching.','de':'Ein laut ausgesprochenes Ja &mdash; nur die Berge sahen zu.','es':'Un sí dicho en voz alta, con solo las montañas mirando.','it':'Un sì detto ad alta voce, con solo le montagne a guardare.'}},
 'official-married-in-the-alps':{
  'lead':{'en':'Legally married on the mountain &mdash; a real registrar, a real certificate, at the top of the Alps.','de':'Rechtsgültig am Berg getraut &mdash; echte Standesbeamtin, echte Urkunde, ganz oben in den Alpen.','es':'Casados legalmente en la montaña &mdash; un registrador real, un certificado real, en lo alto de los Alpes.','it':'Sposati legalmente in montagna &mdash; un ufficiale di stato civile vero, un certificato vero, in cima alle Alpi.'},
  'p1':{'en':'In Austria your wedding on the summit can be the legal one &mdash; a registrar climbs up with you and the marriage you sign for is binding, not symbolic. No paperwork waiting at home; the real thing, thin air and all.','de':'In Österreich kann eure Trauung am Gipfel die rechtsgültige sein &mdash; eine Standesbeamtin steigt mit hinauf, und die Ehe, die ihr unterschreibt, ist bindend, nicht symbolisch. Kein Papierkram, der zu Hause wartet: das Echte, mitsamt dünner Luft.','es':'En Austria vuestra boda en la cima puede ser la legal &mdash; un registrador sube con vosotros y el matrimonio que firmáis es vinculante, no simbólico. Sin papeleo esperando en casa: lo de verdad, con aire fino incluido.','it':'In Austria le vostre nozze in vetta possono essere quelle legali &mdash; un ufficiale sale con voi e il matrimonio che firmate è vincolante, non simbolico. Nessuna burocrazia ad aspettarvi a casa: quello vero, aria sottile compresa.'},
  'p2':{'en':'We arrange the registrar, the permits and the timing, so the only thing you carry up the mountain is the moment itself.','de':'Wir organisieren Standesamt, Genehmigungen und Timing &mdash; das Einzige, was ihr auf den Berg tragt, ist der Moment selbst.','es':'Nos ocupamos del registrador, los permisos y los tiempos, para que lo único que subáis a la montaña sea el momento en sí.','it':'Organizziamo noi l&rsquo;ufficiale, i permessi e i tempi: l&rsquo;unica cosa che portate in montagna è il momento stesso.'},
  'quote':{'en':'Signed, sealed, and a thousand metres closer to the sky.','de':'Unterschrieben, besiegelt &mdash; und tausend Meter näher am Himmel.','es':'Firmado, sellado y mil metros más cerca del cielo.','it':'Firmato, suggellato e mille metri più vicino al cielo.'}},
 'pizza-elopement-at-tre-cime-cadini-di-misurina':{
  'lead':{'en':'Vows at the Cadini di Misurina, near the Tre Cime &mdash; and a celebratory pizza at the top to seal it.','de':'Das Ja an den Cadini di Misurina bei den Drei Zinnen &mdash; und eine Pizza oben drauf zum Feiern.','es':'El sí en los Cadini di Misurina, junto a las Tre Cime &mdash; y una pizza arriba para celebrarlo.','it':'Il sì ai Cadini di Misurina, vicino alle Tre Cime &mdash; e una pizza in vetta per festeggiare.'},
  'p1':{'en':'The Cadini di Misurina are a crowd of slender spires beside the famous Tre Cime di Lavaredo &mdash; one of the great sights of the Dolomites. Up here the couple traded formality for joy, saying their vows on the rock and then splitting a proper Italian pizza with the peaks for a table.','de':'Die Cadini di Misurina sind ein Gewirr schlanker Zinnen neben den berühmten Drei Zinnen &mdash; einer der großen Anblicke der Dolomiten. Hier oben tauschten die beiden Förmlichkeit gegen Freude, gaben sich das Ja am Fels und teilten dann eine echte italienische Pizza, die Gipfel als Tisch.','es':'Los Cadini di Misurina son un enjambre de agujas esbeltas junto a las famosas Tre Cime di Lavaredo &mdash; una de las grandes estampas de los Dolomitas. Aquí arriba la pareja cambió la formalidad por la alegría: se dieron el sí en la roca y compartieron una pizza italiana de verdad, con las cumbres por mesa.','it':'I Cadini di Misurina sono uno stuolo di guglie snelle accanto alle celebri Tre Cime di Lavaredo &mdash; una delle grandi visioni delle Dolomiti. Quassù i due hanno barattato la formalità con la gioia: il sì sulla roccia e poi una vera pizza italiana, con le cime per tavolo.'},
  'p2':{'en':'That is the spirit we love &mdash; a day that is epic and a little bit fun, tradition worn lightly. Bring an appetite; the view is free.','de':'Genau diesen Geist lieben wir &mdash; ein Tag, der episch ist und ein bisschen albern, Tradition leicht getragen. Bringt Appetit mit; die Aussicht gibt es gratis.','es':'Ese es el espíritu que nos encanta &mdash; un día épico y un poco divertido, la tradición llevada con ligereza. Traed apetito; las vistas son gratis.','it':'È lo spirito che amiamo &mdash; una giornata epica e un po&rsquo; scanzonata, la tradizione portata con leggerezza. Portate appetito; il panorama è gratis.'},
  'quote':{'en':'Married at the summit, celebrated with a slice.','de':'Am Gipfel getraut, mit einem Stück Pizza gefeiert.','es':'Casados en la cumbre, celebrado con una porción.','it':'Sposati in vetta, festeggiati con una fetta.'}},
 'sunrise-dolomites-elopement':{
  'lead':{'en':'A pre-dawn hike, then the first sun setting the peaks alight &mdash; a wedding at daybreak.','de':'Ein Aufstieg vor Morgengrauen, dann die erste Sonne, die die Gipfel entzündet &mdash; eine Hochzeit bei Tagesanbruch.','es':'Una caminata antes del alba, y luego el primer sol encendiendo las cumbres &mdash; una boda al amanecer.','it':'Una salita prima dell&rsquo;alba, poi il primo sole che incendia le cime &mdash; nozze allo spuntar del giorno.'},
  'p1':{'en':'They set out in the dark, head-torches on, to be in place when the alpenglow arrives &mdash; those few minutes when the Dolomite walls turn molten pink before the valley has even woken. It is the quietest a great mountain ever gets, and they had it alone.','de':'Sie brachen im Dunkeln auf, Stirnlampen an, um bereit zu sein, wenn das Alpenglühen kommt &mdash; jene wenigen Minuten, in denen die Dolomitenwände glühend rosa werden, ehe das Tal überhaupt erwacht. Stiller wird ein großer Berg nie &mdash; und sie hatten ihn für sich.','es':'Salieron en la oscuridad, con frontales, para estar listos cuando llega el alpenglow &mdash; esos pocos minutos en que las paredes dolomíticas se vuelven rosa incandescente antes de que el valle despierte. Es lo más silencioso que llega a estar una gran montaña, y la tuvieron para ellos.','it':'Sono partiti al buio, con le frontali, per essere pronti all&rsquo;arrivo dell&rsquo;enrosadira &mdash; quei pochi minuti in cui le pareti dolomitiche si fanno rosa incandescente prima ancora che la valle si svegli. È il silenzio più grande che una montagna conosca, e l&rsquo;hanno avuto per loro.'},
  'p2':{'en':'Sunrise asks for an early alarm and warm layers, and gives back light nothing else can match. We scout the spot in advance so the timing is exact.','de':'Sonnenaufgang verlangt einen frühen Wecker und warme Schichten und gibt ein Licht zurück, das nichts sonst erreicht. Wir erkunden den Ort vorab, damit das Timing exakt sitzt.','es':'El amanecer pide despertador temprano y capas de abrigo, y devuelve una luz que nada iguala. Exploramos el lugar de antemano para que los tiempos sean exactos.','it':'L&rsquo;alba chiede una sveglia presto e strati caldi, e restituisce una luce che nulla eguaglia. Studiamo il punto in anticipo perché i tempi siano esatti.'},
  'quote':{'en':'The first light of the day, and the first of a marriage.','de':'Das erste Licht des Tages &mdash; und das erste einer Ehe.','es':'La primera luz del día, y la primera de un matrimonio.','it':'La prima luce del giorno, e la prima di un matrimonio.'}},
 'sunrise-elopement-in-the-dolomites':{
  'lead':{'en':'Alone with the alpenglow &mdash; another daybreak, another summit kept entirely to two.','de':'Allein mit dem Alpenglühen &mdash; ein weiterer Tagesanbruch, ein weiterer Gipfel ganz für zwei.','es':'A solas con el alpenglow &mdash; otro amanecer, otra cima guardada solo para dos.','it':'Soli con l&rsquo;enrosadira &mdash; un altro spuntar del giorno, un&rsquo;altra vetta tutta per due.'},
  'p1':{'en':'There is a reason we keep coming back to sunrise: for one honest hour the Dolomites belong to whoever is willing to lose the sleep. Wrapped against the cold, they watched the colour climb the rock and said the words while the world was still empty.','de':'Es hat einen Grund, warum wir immer wieder zum Sonnenaufgang zurückkehren: für eine ehrliche Stunde gehören die Dolomiten dem, der auf den Schlaf verzichtet. In Decken gegen die Kälte gehüllt, sahen sie die Farbe den Fels erklimmen und sprachen die Worte, während die Welt noch leer war.','es':'Hay una razón por la que volvemos siempre al amanecer: por una hora sincera los Dolomitas son de quien está dispuesto a perder el sueño. Abrigados contra el frío, vieron el color trepar por la roca y dijeron las palabras mientras el mundo seguía vacío.','it':'C&rsquo;è un motivo se torniamo sempre all&rsquo;alba: per un&rsquo;ora sincera le Dolomiti appartengono a chi è disposto a perdere il sonno. Avvolti contro il freddo, hanno visto il colore salire sulla roccia e pronunciato le parole mentre il mondo era ancora vuoto.'},
  'p2':{'en':'A short pre-dawn walk is usually all it takes. What you get for it is solitude money can&rsquo;t buy and light that lasts only minutes.','de':'Ein kurzer Weg vor Morgengrauen genügt meist. Dafür bekommt ihr eine Einsamkeit, die kein Geld kauft, und Licht, das nur Minuten währt.','es':'Suele bastar un corto paseo antes del alba. A cambio recibís una soledad que el dinero no compra y una luz que dura solo minutos.','it':'Di solito basta una breve camminata prima dell&rsquo;alba. In cambio ricevete una solitudine che il denaro non compra e una luce che dura pochi minuti.'},
  'quote':{'en':'Lose an hour of sleep, keep the whole mountain.','de':'Verliert eine Stunde Schlaf, behaltet den ganzen Berg.','es':'Perded una hora de sueño, quedaos con toda la montaña.','it':'Perdete un&rsquo;ora di sonno, tenetevi tutta la montagna.'}},
 'sunset-elopement-tyrol':{
  'lead':{'en':'The other golden hour &mdash; warm Tyrolean light falling long across the ridges.','de':'Die andere goldene Stunde &mdash; warmes Tiroler Licht, das lang über die Grate fällt.','es':'La otra hora dorada &mdash; cálida luz tirolesa cayendo larga sobre las crestas.','it':'L&rsquo;altra ora d&rsquo;oro &mdash; calda luce tirolese che cade lunga sulle creste.'},
  'p1':{'en':'Where sunrise is cool and solitary, sunset is warm and unhurried &mdash; a whole evening softening toward gold. In Tyrol the couple walked up in the afternoon and let the day burn down slowly around them, no alarm and no rush.','de':'Wo der Sonnenaufgang kühl und einsam ist, ist der Sonnenuntergang warm und gemächlich &mdash; ein ganzer Abend, der ins Gold hinüberweicht. In Tirol stieg das Paar am Nachmittag hinauf und ließ den Tag langsam um sich herunterbrennen, ohne Wecker und ohne Eile.','es':'Donde el amanecer es frío y solitario, el atardecer es cálido y sin prisa &mdash; toda una tarde ablandándose hacia el oro. En el Tirol la pareja subió por la tarde y dejó que el día ardiera despacio a su alrededor, sin despertador y sin prisas.','it':'Dove l&rsquo;alba è fredda e solitaria, il tramonto è caldo e senza fretta &mdash; un&rsquo;intera sera che sfuma verso l&rsquo;oro. In Tirolo la coppia è salita nel pomeriggio e ha lasciato che il giorno bruciasse lento intorno a loro, senza sveglia e senza fretta.'},
  'p2':{'en':'Sunset suits couples who&rsquo;d rather not rise in the dark &mdash; the same big light, at a far kinder hour.','de':'Sonnenuntergang passt zu Paaren, die nicht im Dunkeln aufstehen wollen &mdash; dasselbe große Licht, zu einer viel freundlicheren Stunde.','es':'El atardecer va con parejas que prefieren no madrugar en la oscuridad &mdash; la misma gran luz, a una hora mucho más amable.','it':'Il tramonto è ideale per chi preferisce non alzarsi al buio &mdash; la stessa grande luce, a un&rsquo;ora molto più gentile.'},
  'quote':{'en':'The day burned down to gold, and they stayed to watch.','de':'Der Tag brannte zu Gold herunter &mdash; und sie blieben und sahen zu.','es':'El día ardió hasta el oro, y se quedaron a mirar.','it':'Il giorno è bruciato fino all&rsquo;oro, e sono rimasti a guardare.'}},
 'ultimate-italian-elopement':{
  'lead':{'en':'The full Italian Dolomites &mdash; several settings, one unhurried day, la dolce vita at altitude.','de':'Die ganzen italienischen Dolomiten &mdash; mehrere Orte, ein gemächlicher Tag, la dolce vita auf Höhe.','es':'Los Dolomitas italianos al completo &mdash; varios escenarios, un día sin prisa, la dolce vita en altura.','it':'Le Dolomiti italiane al completo &mdash; più scenari, una giornata senza fretta, la dolce vita in quota.'},
  'p1':{'en':'This was the grand version &mdash; not one location but a route through the best of the Italian Dolomites, from lake to pass to peak, threaded together with espresso stops and long views. A day designed to feel less like a shoot and more like the best trip of your lives.','de':'Das war die große Variante &mdash; nicht ein Ort, sondern eine Route durch das Beste der italienischen Dolomiten, von See zu Pass zu Gipfel, verbunden mit Espresso-Pausen und weiten Blicken. Ein Tag, der sich weniger wie ein Shooting anfühlt und mehr wie die schönste Reise eures Lebens.','es':'Esta fue la versión grande &mdash; no un lugar, sino una ruta por lo mejor de los Dolomitas italianos, de lago a puerto a cumbre, hilvanada con paradas de espresso y vistas largas. Un día pensado para sentirse menos como una sesión y más como el mejor viaje de vuestra vida.','it':'Questa era la versione in grande &mdash; non un luogo, ma un itinerario nel meglio delle Dolomiti italiane, dal lago al passo alla vetta, cucito con soste al bar e ampi panorami. Una giornata pensata per sembrare meno un servizio e più il viaggio più bello della vostra vita.'},
  'p2':{'en':'When you have the time to give it, this is how we&rsquo;d spend it &mdash; unrushed, well fed, and moving with the light from morning to last glow.','de':'Wenn ihr die Zeit dafür habt, würden wir sie genau so verbringen &mdash; ohne Hast, gut versorgt, dem Licht folgend von früh bis zum letzten Glühen.','es':'Cuando tenéis el tiempo para dárselo, así lo pasaríamos nosotros &mdash; sin prisa, bien alimentados y siguiendo la luz de la mañana al último resplandor.','it':'Quando avete il tempo da dedicarci, è così che lo passeremmo &mdash; senza fretta, ben nutriti e seguendo la luce dal mattino all&rsquo;ultimo bagliore.'},
  'quote':{'en':'Not a shoot &mdash; the best day of a lifetime, at altitude.','de':'Kein Shooting &mdash; der schönste Tag des Lebens, auf Höhe.','es':'No una sesión &mdash; el mejor día de la vida, en altura.','it':'Non un servizio &mdash; il giorno più bello di sempre, in quota.'}},
}

# --- Bespoke long-form "Journal Feature" for the flagship helicopter story ---
FEAT_HELI_SLUG='adventure-helicopter-elopement-dolomites'
FEATURE_HELI={
 'de':{'kick':'Journal Feature','title':'Helikopter-Elopement in den Dolomiten','by':'von Blitzkneisser',
   'intro':['Ein Elopement in den Dolomiten entscheidet man nicht, weil dabei schöne Bilder entstehen. Man entscheidet es, weil man verstanden hat, was ein Hochzeitstag wirklich sein kann.',
     'Die meisten Hochzeiten folgen einem Drehbuch, das vor Jahren für andere Menschen geschrieben wurde. Gästeliste, Bankett, Sitzordnung, Programm. Ein Tag voller Pflichten, an dessen Ende Braut und Bräutigam erschöpft sind und sich kaum erinnern, wann sie zuletzt wirklich miteinander gesprochen haben.',
     'Jasmi und Dominik wollten das nicht. Deshalb der Helikopter. Deshalb der 6. Juni. Deshalb diese Bilder, die nicht wie eine Hochzeit aussehen &ndash; sondern wie das Leben.'],
   's2h':'Warum die Dolomiten nicht für jeden sind',
   's2':['Ein Elopement in den Dolomiten ist das Gegenteil von Pflichterfüllung. Es ist die Entscheidung, den Tag nicht zu organisieren, sondern zu erleben. Kein Zeitplan, der euch durch die Stunden hetzt, keine Erwartungen, die erfüllt werden wollen &mdash; nur ihr, das Licht und die Stille.',
     'Diese Berge verlangen etwas. Ein frühes Aufstehen, ein Ja zum Wetter, den Mut, den großen Bahnhof gegen einen einzigen ehrlichen Moment zu tauschen. Wer das nicht will, ist hier falsch. Wer es will, bekommt einen Tag, der ihm ganz allein gehört.',
     'Der Helikopter ist dabei nicht der Luxus, sondern die Abkürzung: Minuten statt Stunden, ein Gipfel, den sonst kaum jemand betritt, und die Gewissheit, ihn für euch allein zu haben. Was bleibt, sind keine Programmpunkte &mdash; sondern Bilder, die sich anfühlen wie eine Erinnerung, nicht wie eine Inszenierung.']},
 'en':{'kick':'Journal Feature','title':'Helicopter Elopement in the Dolomites','by':'by Blitzkneisser',
   'intro':['You don&rsquo;t choose to elope in the Dolomites because it makes for beautiful pictures. You choose it because you have understood what a wedding day can really be.',
     'Most weddings follow a script written years ago, for other people. Guest list, banquet, seating plan, running order. A day full of obligations, at the end of which the couple are exhausted and can barely remember the last time they truly spoke to each other.',
     'Jasmi and Dominik didn&rsquo;t want that. That is why the helicopter. That is why the 6th of June. That is why these pictures don&rsquo;t look like a wedding &ndash; they look like life.'],
   's2h':'Why the Dolomites aren&rsquo;t for everyone',
   's2':['Eloping in the Dolomites is the opposite of ticking boxes. It is the decision to live the day rather than organise it. No timetable rushing you through the hours, no expectations to meet &mdash; only the two of you, the light and the silence.',
     'These mountains ask something of you. An early start, a yes to whatever the weather brings, the courage to trade the big production for a single honest moment. If that isn&rsquo;t what you want, this isn&rsquo;t for you. If it is, you get a day that belongs entirely to you.',
     'The helicopter isn&rsquo;t the luxury here &mdash; it is the shortcut: minutes instead of hours, a summit almost no one sets foot on, and the certainty that it is yours alone. What remains are not agenda points, but pictures that feel like a memory, not a staging.']},
 'es':{'kick':'Journal Feature','title':'Elopement en helicóptero en los Dolomitas','by':'por Blitzkneisser',
   'intro':['No se decide un elopement en los Dolomitas porque salgan fotos bonitas. Se decide porque se ha entendido lo que un día de boda puede llegar a ser de verdad.',
     'La mayoría de las bodas siguen un guion escrito hace años, para otras personas. Lista de invitados, banquete, plano de mesas, programa. Un día lleno de obligaciones al final del cual los novios están agotados y apenas recuerdan cuándo hablaron de verdad por última vez.',
     'Jasmi y Dominik no querían eso. Por eso el helicóptero. Por eso el 6 de junio. Por eso estas fotos no parecen una boda &ndash; parecen la vida.'],
   's2h':'Por qué los Dolomitas no son para todos',
   's2':['Un elopement en los Dolomitas es lo contrario de cumplir un trámite. Es la decisión de vivir el día en lugar de organizarlo. Sin un horario que os apremie, sin expectativas que satisfacer &mdash; solo vosotros dos, la luz y el silencio.',
     'Estas montañas piden algo. Madrugar, decir sí al tiempo que haga, el valor de cambiar el gran montaje por un único momento sincero. Si no es lo que queréis, no es para vosotros. Si lo es, tendréis un día que os pertenece por completo.',
     'El helicóptero no es aquí el lujo &mdash; es el atajo: minutos en vez de horas, una cumbre que casi nadie pisa y la certeza de tenerla solo para vosotros. Lo que queda no son puntos de un programa, sino imágenes que se sienten como un recuerdo, no como una puesta en escena.']},
 'it':{'kick':'Journal Feature','title':'Elopement in elicottero nelle Dolomiti','by':'di Blitzkneisser',
   'intro':['Non si sceglie un elopement nelle Dolomiti perché ne escono belle foto. Lo si sceglie perché si è capito che cosa può essere davvero un giorno di nozze.',
     'La maggior parte dei matrimoni segue un copione scritto anni fa, per altre persone. Lista degli invitati, banchetto, disposizione dei tavoli, programma. Una giornata piena di doveri, al termine della quale gli sposi sono esausti e faticano a ricordare l&rsquo;ultima volta in cui si sono davvero parlati.',
     'Jasmi e Dominik non volevano questo. Per questo l&rsquo;elicottero. Per questo il 6 giugno. Per questo queste immagini non sembrano un matrimonio &ndash; sembrano la vita.'],
   's2h':'Perché le Dolomiti non sono per tutti',
   's2':['Un elopement nelle Dolomiti è l&rsquo;opposto di un dovere da assolvere. È la scelta di vivere la giornata invece di organizzarla. Nessun programma che vi incalza tra le ore, nessuna aspettativa da soddisfare &mdash; solo voi due, la luce e il silenzio.',
     'Queste montagne chiedono qualcosa. Una sveglia presto, un sì al tempo che verrà, il coraggio di scambiare la grande messinscena con un unico momento sincero. Se non è ciò che volete, non fa per voi. Se lo è, avrete una giornata che vi appartiene per intero.',
     'Qui l&rsquo;elicottero non è il lusso &mdash; è la scorciatoia: minuti anziché ore, una vetta su cui quasi nessuno mette piede e la certezza di averla solo per voi. Ciò che resta non sono punti di un programma, ma immagini che sembrano un ricordo, non una messa in scena.']},
}

def feature_heli(lang,P,slug,img,alt):
    F=FEATURE_HELI[lang]
    srcs=[f'{P}img/gallery/{slug}/{fn}' for fn in _gallery_files(slug)[:MAX_GALLERY]]
    g1=[srcs[i] for i in (0,2,3,4) if i<len(srcs)]   # Galerie 1: Bilder 1, 3, 4, 5
    g2=srcs[5:]                                       # Galerie 2: Bilder 6 ff.
    intro=''.join((f'<p class="dropcap">{p}</p>' if k==0 else f'<p>{p}</p>') for k,p in enumerate(F['intro']))
    s2=''.join(f'<p>{p}</p>' for p in F['s2'])
    return (
      f'<section class="page-hero" style="padding:0"><div class="bg" style="background-image:url(\'{P}img/stories/{img}.webp\')"></div>'
      f'<div class="content"><div class="wrap"><div class="kicker" data-n="{F["kick"]}"><span class="line"></span></div><h1>{F["title"]}</h1></div></div></section>'
      f'<div class="page-plain" style="border-top:0"><div class="wrap"><div class="pi-intro reveal">'
      f'<div class="byline">{F["by"]}</div>{intro}</div></div></div>'
      '<section><div class="wide">'+_render_gallery(g1,alt,full=True)+'</div></section>'
      f'<section style="padding-top:clamp(30px,5vw,64px)"><div class="wrap"><div class="pi-intro reveal">'
      f'<h2 class="feat-h2">{F["s2h"]}</h2>{s2}</div></div></section>'
      +('<section><div class="wide">'+_render_gallery(g2,alt,full=True)+'</div></section>' if g2 else ''))

def build_portfolio(lang):
    for s in STORIES:
        num,slug,img,cats,titles=s
        rel=f'portfolio-item/{slug}/'; P=prefix(lang,rel)
        catlinks=' &middot; '.join(f'<a href="{u(P,lang,"portfolio-category/"+c+"/")}" style="color:inherit">{catname(c,lang)}</a>' for c in cats)
        st=PI_TEXT.get(slug)
        lead=st['lead'][lang] if st else t(lang,'pi_lead')
        p1  =st['p1'][lang]   if st else t(lang,'pi_p')
        p2  =st['p2'][lang]   if st else ''
        quote=st['quote'][lang] if st else ''
        bodyhtml=f'<p class="dropcap">{p1}</p>'+(f'<p>{p2}</p>' if p2 else '')
        credits=(f'{t(lang,"pi_vplan")} <a class="partner-inline" href="{P_PLAN[1]}" target="_blank" rel="noopener">Dolomites Wedding Planner</a> &middot; '
          f'{t(lang,"f_role_photo")} <a class="partner-inline" href="https://hochzeitsfotograf.tirol" target="_blank" rel="noopener">Blitzkneisser</a>')
        if slug==FEAT_HELI_SLUG:
            main=feature_heli(lang,P,slug,img,titles[lang])
        else:
            main=(
              f'<section class="page-hero" style="padding:0"><div class="bg" style="background-image:url(\'{P}img/stories/{img}.webp\')"></div>'
              f'<div class="content"><div class="wrap"><div class="kicker" data-n="Story N&deg;{num:02d}"><span class="line"></span></div><h1>{titles[lang]}</h1></div></div></section>'
              f'<div class="page-plain" style="border-top:0"><div class="wrap"><div class="pi-intro reveal">'
              f'<div class="cap" style="margin-bottom:16px">{catlinks}</div>'
              f'<p class="lead pi-lead">{lead}</p>{bodyhtml}'
              f'<p class="small pi-credits">{credits}</p>'
              f'<div class="gal-head reveal"><span>{t(lang,"pi_gallery")}</span></div></div></div></div>'
              '<section><div class="gallery-wrap">'+gallery_html(lang,P,slug,titles[lang],quote)+'</div></section>'
              f'<section class="pi-outro"><div class="wrap reveal"><p>{t(lang,"pi_outro")}</p></div></section>')
        body=(nav(lang,rel,'stories')+main+
          '<section class="cta"><div class="wrap row reveal"><div>'
          f'<div class="kicker" data-n="{t(lang,"pi_your")}"><span class="line"></span></div><h2 style="margin-top:20px">{t(lang,"pi_cta_h")}</h2></div>'
          f'<a href="{u(P,lang,"get-in-touch/")}" class="btn light">{t(lang,"start_planning")}</a></div></section>'
          +footer(lang,rel)+
          '<div class="lb" id="lb"><span class="x" id="lbx">&times;</span><span class="arw prev" id="lbp">&lsaquo;</span><img id="lbimg" src="" alt=""><span class="arw next" id="lbn">&rsaquo;</span></div>')
        img_ld={"@context":"https://schema.org","@type":"ImageObject",
            "contentUrl":f'{DOMAIN}/img/stories/{img}.webp',"name":_plain(titles[lang]),
            "representativeOfPage":True,"creator":{"@id":ORG_ID}}
        write(lang,rel,head(lang,rel,f'{titles[lang]} — Mountain Elopement',DESC['stories'][lang],img_ld)+body+scripts(P,LB_JS))

def build_packages(lang):
    rel='our-packages/'; P=prefix(lang,rel)
    hrs=t(lang,'pk_hours'); ph=t(lang,'pk_photos')
    badge={'en':'Most chosen','de':'Beliebteste Wahl','es':'La más elegida','it':'La più scelta'}[lang]
    def tier(no,label,name,price,items,feat=False,tag=''):
        cls='tier feat' if feat else 'tier'
        lis=''.join('<li>'+i+'</li>' for i in items)
        bdg=f'<div class="badge">{badge}</div>' if feat else ''
        tg=f'<div class="tier-tag">{tag}</div>' if tag else ''
        eurnum=price.replace('.','')   # raw EUR value for the indicative USD conversion
        return (f'<div class="{cls}">{bdg}<div class="no">N&deg;{no} &mdash; {label}</div><div class="name">{name}</div>{tg}'
          f'<div class="price" data-eur="{eurnum}"><span class="cur">&euro;</span><span class="amt">{price}</span></div><ul>{lis}</ul>'
          f'<a href="{u(P,lang,"get-in-touch/")}" class="tier-cta">{t(lang,"request")} &rarr;</a></div>')
    photoword={'en':'Photography','de':'Fotografie','es':'Fotografía','it':'Fotografia'}[lang]
    gr={'en':'Getting ready','de':'Getting Ready','es':'Preparativos','it':'Preparativi'}[lang]
    gropt={'en':'Getting ready (optional)','de':'Getting Ready (optional)','es':'Preparativos (opcional)','it':'Preparativi (opzionale)'}[lang]
    loc={'en':'Location scouting','de':'Location-Scouting','es':'Búsqueda de localización','it':'Sopralluogo location'}[lang]
    concept={'en':'Concept & idea','de':'Konzept & Idee','es':'Concepto e idea','it':'Concept e idea'}[lang]
    flowers={'en':'Flowers · Hair & Make-up','de':'Blumen · Hair & Make-up','es':'Flores · Peluquería y maquillaje','it':'Fiori · Trucco e acconciatura'}[lang]
    locplan={'en':'Location · Organisation & planning','de':'Location · Organisation & Planung','es':'Localización · Organización y planificación','it':'Location · Organizzazione e pianificazione'}[lang]
    fullplan={'en':'Full planning: accommodation, reception, transfers','de':'Komplette Planung: Unterkunft, Empfang, Transfers','es':'Planificación completa: alojamiento, recepción, traslados','it':'Pianificazione completa: alloggio, ricevimento, trasferimenti'}[lang]
    # deliverables articulated the way competitors list them (adds perceived value, no extra cost)
    imgword={'en':'edited images','de':'bearbeitete Bilder','es':'imágenes editadas','it':'immagini modificate'}[lang]
    gallery={'en':'Private online gallery &mdash; preview in 1 week','de':'Private Online-Galerie &mdash; Vorschau in 1 Woche','es':'Galería online privada &mdash; vista previa en 1 semana','it':'Galleria online privata &mdash; anteprima in 1 settimana'}[lang]
    planningcall={'en':'Planning call & personal timeline','de':'Planungscall & persönliche Timeline','es':'Llamada de planificación y cronograma','it':'Call di pianificazione e timeline'}[lang]
    weather={'en':'Weather backup day','de':'Wetter-Ausweichtag','es':'Día alternativo por el clima','it':'Giorno di riserva meteo'}[lang]
    permits={'en':'Permits & logistics handled','de':'Genehmigungen & Logistik übernommen','es':'Permisos y logística incluidos','it':'Permessi e logistica inclusi'}[lang]
    album={'en':'Heirloom album','de':'Erinnerungsalbum','es':'Álbum de recuerdo','it':'Album ricordo'}[lang]
    tag1={'en':'Just the two of you and the mountains.','de':'Nur ihr beide und die Berge.','es':'Solo vosotros dos y las montañas.','it':'Solo voi due e le montagne.'}[lang]
    tag2={'en':'A fuller day, beautifully held.','de':'Ein voller Tag, rundum begleitet.','es':'Un día completo, bien acompañado.','it':'Una giornata intera, ben accompagnata.'}[lang]
    tag3={'en':'The whole day, fully planned.','de':'Der ganze Tag, komplett geplant.','es':'Todo el día, totalmente planificado.','it':'L\'intera giornata, tutto pianificato.'}[lang]
    t1=tier('01',t(lang,'pk_l1'),t(lang,'pk_t1'),'6.000',[f'{photoword} &mdash; 50&ndash;80 {imgword}',f'2&ndash;3 {hrs}',loc,concept,planningcall,gallery],tag=tag1)
    t2=tier('02',t(lang,'pk_l2'),t(lang,'pk_t2'),'9.000',[f'{photoword} &mdash; 80&ndash;100 {imgword}',f'4&ndash;5 {hrs}',gropt,flowers,locplan,planningcall,weather,gallery],feat=True,tag=tag2)
    t3=tier('03',t(lang,'pk_l3'),t(lang,'pk_t3'),'13.500',[f'{photoword} &mdash; 100&ndash;200 {imgword}',f'6&ndash;8 {hrs}',gr,flowers,fullplan,permits,weather,album,gallery],tag=tag3)
    def ad(name,price): return f'<div class="addon"><div class="a">{name}</div><div class="p">{price}</div></div>'
    addons=(ad(t(lang,'ad_heli'),'&asymp; &euro; 2.500')
      +ad(t(lang,'ad_film'),'&asymp; &euro; 3.500')
      +ad(t(lang,'ad_civil'),'&asymp; &euro; 1.000')+ad(t(lang,'ad_celeb'),'&asymp; &euro; 1.500')
      +ad(t(lang,'ad_cake'),f'{t(lang,"ad_from")} &euro; 400')+ad(t(lang,'ad_music'),'&asymp; &euro; 600')
      +ad(f'<a href="{P_MUA[1]}" target="_blank" rel="noopener" style="color:inherit">{t(lang,"ad_mua")}</a>',t(lang,'ad_onreq'))
      +ad(t(lang,'ad_backdrop'),'&euro; 600'))
    eurnote={'en':'All prices in EUR.','de':'Alle Preise in EUR.','es':'Todos los precios en EUR.','it':'Tutti i prezzi in EUR.'}[lang]
    fxnote={'en':'Indicative — the binding price is in EUR. Rates update daily.',
            'de':'Indikativ — verbindlich ist der EUR-Preis. Kurse aktualisieren sich täglich.',
            'es':'Orientativo — el precio vinculante es en EUR. Los tipos se actualizan a diario.',
            'it':'Indicativo — il prezzo vincolante è in EUR. I tassi si aggiornano ogni giorno.'}[lang]
    curswitch=('<div class="cur-switch-row reveal"><div class="cur-switch" role="group" aria-label="Currency">'
      '<button type="button" data-cur="EUR" class="on">EUR</button>'
      '<button type="button" data-cur="USD">USD</button>'
      '<button type="button" data-cur="GBP">GBP</button></div></div>')
    # Currency switcher: EUR is the base/binding price; USD & GBP are converted client-side
    # from a live ECB rate. Foreign buttons stay disabled until the rate loads (no wrong numbers).
    curjs=('<script>(function(){var sw=document.querySelector(".cur-switch");if(!sw)return;'
      'var prices=document.querySelectorAll(".price[data-eur]"),note=document.querySelector(".cur-note"),btns=sw.querySelectorAll("button");'
      'var rates={EUR:1},sym={EUR:"\\u20ac",USD:"$",GBP:"\\u00a3"},loc={EUR:"de-DE",USD:"de-DE",GBP:"de-DE"};'
      'function fmt(cur){prices.forEach(function(p){var eur=parseFloat(p.getAttribute("data-eur")),c=p.querySelector(".cur"),a=p.querySelector(".amt"),amt;'
      'if(cur==="EUR"){amt=eur;}else{var r=rates[cur];if(!r)return;amt=Math.round(eur*r/100)*100;}'
      'c.textContent=sym[cur];a.textContent=amt.toLocaleString(loc[cur]);});'
      'if(note)note.textContent=note.getAttribute(cur==="EUR"?"data-eur-note":"data-fx-note");}'
      'function setCur(cur){btns.forEach(function(b){b.classList.toggle("on",b.getAttribute("data-cur")===cur);});fmt(cur);try{localStorage.setItem("me_cur",cur);}catch(e){}}'
      'btns.forEach(function(b){b.addEventListener("click",function(){var c=b.getAttribute("data-cur");if(c!=="EUR"&&!rates[c])return;setCur(c);});'
      'if(b.getAttribute("data-cur")!=="EUR")b.disabled=true;});'
      'setCur("EUR");'
      'fetch("https://api.frankfurter.dev/v1/latest?base=EUR&symbols=USD,GBP").then(function(r){return r.json();}).then(function(d){'
      'if(d&&d.rates){rates.USD=d.rates.USD;rates.GBP=d.rates.GBP;btns.forEach(function(b){b.disabled=false;});'
      'var s;try{s=localStorage.getItem("me_cur");}catch(e){}if(s&&rates[s])setCur(s);}}).catch(function(){});'
      '})();</script>')
    body=(nav(lang,rel,'packages')+
      f'<div class="page-plain"><div class="wrap"><div class="kicker" data-n="{t(lang,"pk_k")}"><span class="line"></span></div>'
      f'<h1>{t(lang,"pk_h")}</h1><p class="lead">{t(lang,"pk_lead")}</p></div></div>'
      f'<section><div class="wrap">{curswitch}<div class="tiers reveal">{t1}{t2}{t3}</div>'
      f'<p class="small reveal cur-note" data-eur-note="{eurnote}" data-fx-note="{fxnote}" style="margin-top:18px;color:var(--ink-2)">{eurnote}</p>'
      f'<p class="lead reveal" style="max-width:760px;margin-top:clamp(32px,4vw,52px)">{t(lang,"pk_note")}</p>'
      f'<div class="section-head reveal" style="margin-top:clamp(40px,6vw,72px)"><div class="kicker" data-n="Add-ons">{t(lang,"pk_addk")}<span class="line"></span></div></div>'
      f'<div class="addons reveal">{addons}</div></div></section>'
      '<section class="band"><div class="wrap quote reveal">'
      f'<div class="kicker" data-n="{t(lang,"pk_band_k")}"><span class="line"></span></div>'
      f'<p style="margin-top:26px">{t(lang,"pk_band_q")}</p><div class="who">Tanja &amp; Andreas &mdash; Mountain Elopement</div></div></section>'
      '<section class="cta"><div class="wrap row reveal"><div>'
      f'<div class="kicker" data-n="{t(lang,"pk_next")}"><span class="line"></span></div><h2 style="margin-top:20px">{t(lang,"pk_cta_h")}</h2></div>'
      f'<a href="{u(P,lang,"get-in-touch/")}" class="btn light">{t(lang,"pk_req_price")}</a></div></section>'
      +footer(lang,rel))
    write(lang,rel,head(lang,rel,TITLES['packages'][lang],DESC['packages'][lang])+body+scripts(P,curjs))

def build_team(lang):
    rel='our-team/'; P=prefix(lang,rel)
    body=(nav(lang,rel,'team')+
      f'<div class="page-plain"><div class="wrap"><div class="kicker" data-n="{t(lang,"tp_k")}"><span class="line"></span></div>'
      f'<h1>{t(lang,"tp_h")}</h1><p class="lead">{t(lang,"tp_lead")}</p></div></div>'
      f'<section><div class="wrap feature"><div class="media reveal"><img src="{P}img/team/team.webp" alt="Das Team von Mountain Elopement in den Dolomiten">'
      '<div class="caption">Jlenia &amp; Andreas.</div></div><div class="body reveal">'
      f'<div class="kicker" data-n="01">{t(lang,"tp_fk")}<span class="line"></span></div><h2>Jlenia &amp; Andreas</h2>'
      f'<p class="lead">{t(lang,"tp_flead")}</p><p class="dropcap">{t(lang,"tp_fp1")}</p><p>{t(lang,"tp_fp2")}</p>'
      f'<a href="{u(P,lang,"get-in-touch/")}" class="arrow-link">{t(lang,"tp_hello")}</a></div></div></section>'
      +team_section(lang,P)+
      '<section class="cta"><div class="wrap row reveal"><div>'
      f'<div class="kicker" data-n="{t(lang,"tp_cta_k")}"><span class="line"></span></div><h2 style="margin-top:20px">{t(lang,"tp_cta_h")}</h2></div>'
      f'<a href="{u(P,lang,"get-in-touch/")}" class="btn light">{t(lang,"tp_plan")}</a></div></section>'
      +footer(lang,rel))
    write(lang,rel,head(lang,rel,TITLES['team'][lang],DESC['team'][lang])+body+scripts(P))

def build_contact(lang):
    rel='get-in-touch/'; P=prefix(lang,rel)
    chips=''.join(f'<span class="chip">{c}</span>' for c in T['chips'][lang])
    thankyou=f'/{lbase(lang)}thank-you-for-your-inquiry/'
    chip_js=("<script>var box=document.getElementById('chips');box.addEventListener('click',function(e){"
           "if(e.target.classList.contains('chip')){e.target.classList.toggle('on');"
           "var h=document.getElementById('interests');if(h)h.value=[].slice.call(box.querySelectorAll('.chip.on'))"
           ".map(function(x){return x.textContent;}).join(', ');}});</script>")
    ts_api='<script src="https://challenges.cloudflare.com/turnstile/v0/api.js" async defer></script>'
    submit_js=(
      "<script>(function(){var f=document.getElementById('ce-form');if(!f)return;"
      "var st=document.getElementById('ce-status'),btn=f.querySelector('button[type=submit]');"
      "var THANKYOU="+json.dumps(thankyou)+";"
      "var MSG={sending:"+json.dumps(t(lang,'ct_sending'))+",ok:"+json.dumps(t(lang,'ct_ok'))+",err:"+json.dumps(t(lang,'ct_err'))+"};"
      "f.addEventListener('submit',function(e){e.preventDefault();"
      "var box=document.getElementById('chips'),h=document.getElementById('interests');"
      "if(box&&h)h.value=[].slice.call(box.querySelectorAll('.chip.on')).map(function(x){return x.textContent;}).join(', ');"
      "btn.disabled=true;st.className='ce-status sending';st.textContent=MSG.sending;"
      "fetch("+json.dumps(CONTACT_ENDPOINT)+",{method:'POST',body:new FormData(f)})"
      ".then(function(r){return r.json().catch(function(){return {ok:r.ok};});})"
      ".then(function(d){if(d&&d.ok){st.className='ce-status ok';st.textContent=MSG.ok;window.location.href=THANKYOU;}"
      "else{st.className='ce-status err';st.textContent=(d&&d.error)||MSG.err;btn.disabled=false;if(window.turnstile)turnstile.reset();}})"
      ".catch(function(){st.className='ce-status err';st.textContent=MSG.err;btn.disabled=false;if(window.turnstile)turnstile.reset();});"
      "});})();</script>")
    extra=chip_js+ts_api+submit_js
    body=(nav(lang,rel,'contact')+
      f'<div class="page-plain"><div class="wrap"><div class="kicker" data-n="{t(lang,"ct_k")}"><span class="line"></span></div>'
      f'<h1>{t(lang,"ct_h")}</h1><p class="lead">{t(lang,"ct_lead")}</p></div></div>'
      f'<section><div class="wrap contact-grid"><form id="ce-form" class="form reveal" name="contact" method="POST" action="{CONTACT_ENDPOINT}">'
      '<input type="hidden" name="form-name" value="contact">'
      f'<input type="hidden" name="language" value="{lang}">'
      '<p hidden aria-hidden="true"><label>Don&rsquo;t fill this out if you&rsquo;re human: <input name="bot-field"></label></p>'
      f'<div class="kicker" data-n="01" style="margin-bottom:22px">{t(lang,"ct_details")}<span class="line"></span></div>'
      f'<label>{t(lang,"ct_name")}</label><input type="text" name="name" placeholder="{t(lang,"ct_name_ph")}" required>'
      f'<label>{t(lang,"ct_email")}</label><input type="email" name="email" placeholder="you@email.com" required>'
      f'<label>{t(lang,"ct_date")}</label><input type="text" name="date" placeholder="{t(lang,"ct_date_ph")}">'
      f'<label>{t(lang,"ct_dream")}</label><div class="chips" id="chips">{chips}</div><input type="hidden" name="interests" id="interests">'
      f'<label>{t(lang,"ct_story")}</label><textarea name="message" rows="5" placeholder="{t(lang,"ct_story_ph")}" required></textarea>'
      f'<div class="cf-turnstile" data-sitekey="{TURNSTILE_SITEKEY}" data-theme="light" style="margin:8px 0 18px"></div>'
      f'<button class="btn" type="submit">{t(lang,"ct_send")}</button>'
      '<p id="ce-status" class="ce-status" role="status" aria-live="polite"></p>'
      '</form>'
      f'<aside class="contact-side reveal"><img src="{P}img/page/contact.webp" alt="Mountain Elopement">'
      '<div class="info"><div><strong>Email</strong> &mdash; hello@mountain-elopement.com</div>'
      '<div><strong>WhatsApp</strong> &mdash; +39 348 425 8317</div>'
      f'<div><strong>{t(lang,"ct_based")}</strong> &mdash; {t(lang,"ct_based_v")}</div>'
      '<div><strong>Instagram</strong> &mdash; @mountainelopement</div></div></aside></div></section>'
      +footer(lang,rel))
    write(lang,rel,head(lang,rel,TITLES['contact'][lang],DESC['contact'][lang])+body+scripts(P,extra))

def build_thankyou(lang):
    # noindex confirmation page — kept out of sitemap; likely carries GTM conversion tracking
    rel='thank-you-for-your-inquiry/'; P=prefix(lang,rel)
    body=(nav(lang,rel,'')+
      f'<div class="page-plain"><div class="wrap"><div class="kicker" data-n="{t(lang,"ty_k")}"><span class="line"></span></div>'
      f'<h1>{t(lang,"ty_h")}</h1><p class="lead">{t(lang,"ty_p")}</p>'
      f'<p style="margin-top:1.6em"><a href="{u(P,lang,"")}" class="btn light">{t(lang,"ty_home")}</a></p></div></div>'
      +footer(lang,rel))
    write(lang,rel,head(lang,rel,TITLES['thankyou'][lang],DESC['thankyou'][lang],noindex=True)+body+scripts(P))

def build_legal(lang):
    for slug,key in [('imprint','lg_imprint'),('privacy-policy','lg_privacy')]:
        rel=f'{slug}/'; P=prefix(lang,rel)
        title=t(lang,key)
        body=(nav(lang,rel,'')+
          f'<div class="page-plain"><div class="wrap"><div class="kicker" data-n="{t(lang,"lg_k")}"><span class="line"></span></div>'
          f'<h1>{title}</h1><p class="lead">{t(lang,"lg_lead")}</p></div></div>'
          '<section><div class="wrap"><p style="max-width:720px;color:var(--ink-2)">1:1</p></div></section>'+footer(lang,rel))
        write(lang,rel,head(lang,rel,f'{title} — Mountain Elopement','')+body+scripts(P))

def guide_card(lang,P,g):
    return (f'<a class="st reveal" href="{u(P,lang,"how-to-elope-in-the-europe-mountains/"+g["slug"]+"/")}">'
        f'<div class="imgwrap"><img src="{P}img/stories/{g["img"]}.webp" alt="{g["title"][lang]}"></div>'
        f'<div class="no">{t(lang,"guide_kick")}</div><h3>{g["title"][lang]}</h3>'
        f'<div class="tags" style="text-transform:none;letter-spacing:0;font-family:var(--serif);font-style:italic;font-size:15px">{g["excerpt"][lang]}</div></a>')

def guide_map(lang,P):
    pins=[('map_tyrol','elope-in-austria',300,300),('map_lakes','best-alps-elopement-locations',540,225),('map_dol','dolomites-elopement-guide',760,345)]
    svg='<div class="guide-map reveal"><svg viewBox="0 0 1000 520" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Region map">'
    svg+='<g fill="none" stroke="var(--line-2)" stroke-width="1" opacity=".5"><path d="M70,150 C260,90 420,180 560,140 S860,120 970,196"/><path d="M55,214 C245,150 430,244 600,202 S890,182 985,258"/></g>'
    svg+='<path d="M0,520 L0,470 L160,438 L300,486 L460,432 L620,482 L780,430 L920,472 L1000,452 L1000,520 Z" fill="var(--line-2)" opacity=".3"/>'
    svg+='<path d="M0,520 L0,432 L120,470 L230,386 L330,452 L430,362 L540,442 L650,354 L760,430 L870,374 L1000,442 L1000,520 Z" fill="var(--line)" opacity=".5"/>'
    svg+='<path d="M300,300 L540,225 L760,345" fill="none" stroke="var(--line-2)" stroke-width="1.5" stroke-dasharray="3 7"/>'
    for lk,slug,x,y in pins:
        href=u(P,lang,'how-to-elope-in-the-europe-mountains/'+slug+'/')
        svg+=(f'<a href="{href}"><g class="gm-pin"><circle class="ring" cx="{x}" cy="{y}" r="10"></circle>'
              f'<circle class="dot" cx="{x}" cy="{y}" r="8"></circle>'
              f'<text x="{x}" y="{y-22}" text-anchor="middle">{t(lang,lk)}</text></g></a>')
    svg+='</svg></div>'
    return svg

# --- Guide hub: filterable "Start Here" grid (topic chips) ---
GCAT_ORDER=['all','dolomites','locations','seasons','planning']
GCAT={
 'all':{'en':'All guides','de':'Alle Guides','es':'Todas las guías','it':'Tutte le guide'},
 'dolomites':{'en':'Dolomites','de':'Dolomiten','es':'Dolomitas','it':'Dolomiti'},
 'tyrol':{'en':'Tyrol','de':'Tirol','es':'Tirol','it':'Tirolo'},
 'locations':{'en':'Locations','de':'Orte','es':'Lugares','it':'Luoghi'},
 'seasons':{'en':'Seasons','de':'Jahreszeiten','es':'Estaciones','it':'Stagioni'},
 'civil':{'en':'Civil wedding','de':'Standesamt','es':'Boda civil','it':'Matrimonio civile'},
 'planning':{'en':'Planning','de':'Planung','es':'Planificación','it':'Pianificazione'},
}
GUIDE_CATS={
 'dolomites-elopement-guide':['dolomites','locations','seasons'],
 'elope-in-austria':['locations'],
 'best-alps-elopement-locations':['dolomites','locations'],
 'how-to-plan-your-elopement':['planning'],
 'most-beautiful-dolomites-spots':['dolomites','locations'],
 'helicopter-elopement-dolomites-guide':['dolomites','locations','planning'],
 'mountain-proposal-guide':['planning','locations','seasons'],
 'sunrise-or-sunset-elopement':['seasons','planning'],
 'elopement-things-nobody-tells-you':['planning','seasons'],
}
GUIDE_JS=("<script>(function(){var f=document.getElementById('guideFilters');if(!f)return;"
 "var cards=[].slice.call(document.querySelectorAll('#guideGrid [data-cat]'));"
 "f.addEventListener('click',function(e){var b=e.target.closest('button[data-filter]');if(!b)return;"
 "f.querySelectorAll('button').forEach(function(x){x.setAttribute('aria-pressed',x===b?'true':'false');});"
 "var c=b.getAttribute('data-filter');cards.forEach(function(k){var m=c==='all'||((' '+k.getAttribute('data-cat')+' ').indexOf(' '+c+' ')>-1);k.style.display=m?'':'none';});});})();</script>")

def guide_hub(lang,P):
    present=[c for c in GCAT_ORDER if c=='all' or any(c in GUIDE_CATS.get(g['slug'],[]) for g in GUIDES)]
    chips=''.join(f'<button type="button" class="gchip" data-filter="{c}" aria-pressed="{"true" if c=="all" else "false"}">{GCAT[c][lang]}</button>' for c in present)
    cards=''
    for g in GUIDES:
        cats=' '.join(GUIDE_CATS.get(g['slug'],[]))
        href=u(P,lang,'how-to-elope-in-the-europe-mountains/'+g['slug']+'/')
        cards+=(f'<a class="gcard reveal" data-cat="{cats}" href="{href}">'
                f'<div class="imgwrap"><img src="{P}img/stories/{g["img"]}.webp" alt="{g["title"][lang]}" loading="lazy"></div>'
                f'<div class="no">{t(lang,"guide_kick")}</div><h3>{g["title"][lang]}</h3>'
                f'<div class="gcard-x">{g["excerpt"][lang]}</div></a>')
    return ('<div class="page-plain" style="border-bottom:0"><div class="wrap">'
            f'<div class="kicker" data-n="{t(lang,"gd_k")}"><span class="line"></span></div>'
            f'<h1>{t(lang,"gd_h")}</h1><p class="lead">{t(lang,"ht_start_copy")}</p>'
            f'<div class="guide-filters" id="guideFilters" aria-label="Guide filters">{chips}</div></div></div>'
            f'<section style="padding-top:clamp(24px,3vw,40px)"><div class="wrap"><div class="guide-grid" id="guideGrid">{cards}</div></div></section>')

def guide_mosaic(lang,P):
    cls=['m-tile m-w','m-tile m-n','m-tile m-n','m-tile m-w']
    tiles=''
    for i,g in enumerate(GUIDES):
        c=cls[i] if i<len(cls) else 'm-tile'
        href=u(P,lang,'how-to-elope-in-the-europe-mountains/'+g['slug']+'/')
        tiles+=(f'<a class="{c} reveal" href="{href}"><img src="{P}img/stories/{g["img"]}.webp" alt="{g["title"][lang]}">'
                f'<div class="m-cap"><div class="m-cat">{t(lang,"guide_kick")}</div><h3>{g["title"][lang]}</h3></div></a>')
    return '<div class="mosaic">'+tiles+'</div>'

def linkify(text,lang,P):
    """Turn [[g:slug|label]] / [[s:slug|label]] / [[c:cat|label]] tokens into internal links."""
    def _r(m):
        k,slug,label=m.group(1),m.group(2),m.group(3)
        rel={'g':'how-to-elope-in-the-europe-mountains/'+slug+'/',
             's':'portfolio-item/'+slug+'/',
             'c':'portfolio-category/'+slug+'/'}.get(k)
        return f'<a href="{u(P,lang,rel)}">{label}</a>' if rel else label
    return re.sub(r'\[\[([gsc]):([a-z0-9-]+)\|([^\]|]+)\]\]',_r,text)

def build_guides(lang):
    for g in GUIDES:
        ex=GUIDE_EXTRA[g['slug']]
        rel='how-to-elope-in-the-europe-mountains/'+g['slug']+'/'; P=prefix(lang,rel)
        facts='<div class="facts">'+''.join(f'<div class="fct"><div class="fl">{LBL[k][lang]}</div><div class="fv">{val[lang]}</div></div>' for k,val in ex['facts'])+'</div>'
        allsec=g['sec']+[ex['sec4']]
        secs=''
        for s in allsec:
            secs+=(f'<h2 style="font-family:var(--serif);font-weight:400;font-size:clamp(25px,3vw,36px);letter-spacing:-.01em;margin:1.5em 0 .35em">{s["h"][lang]}</h2>'
                   f'<p style="color:var(--ink-2)">{linkify(s["p"][lang],lang,P)}</p>')
        tips='<div class="tips"><h4>'+t(lang,'good_to_know')+'</h4><ul>'+''.join('<li>'+linkify(it,lang,P)+'</li>' for it in ex['tips'][lang])+'</ul></div>'
        related=''.join(story_card(lang,P,STORYBY[sl]) for sl in ex['stories'])
        more=''.join(guide_card(lang,P,x) for x in GUIDES if x['slug']!=g['slug'])
        body=(nav(lang,rel,'howto')+
          f'<section class="page-hero" style="padding:0"><div class="bg" style="background-image:url(\'{P}img/stories/{g["img"]}.webp\')"></div>'
          f'<div class="content"><div class="wrap"><div class="kicker" data-n="{t(lang,"guide_kick")}"><span class="line"></span></div><h1>{g["title"][lang]}</h1></div></div></section>'
          '<section><div class="wrap" style="max-width:820px">'
          f'<p class="lead">{linkify(g["intro"][lang],lang,P)}</p>'
          f'<div class="cap" style="margin:0 0 -14px">{t(lang,"quick_facts")}</div>{facts}'
          f'{secs}{tips}'
          f'<p style="margin-top:2.4em"><a href="{u(P,lang,"how-to-elope-in-the-europe-mountains/")}" class="arrow-link">&larr; {T["nav"]["howto"][lang]}</a></p></div></section>'
          '<section style="padding-top:0"><div class="wrap"><div class="section-head reveal">'
          f'<div class="kicker" data-n="{t(lang,"related_stories")}"><span class="line"></span></div><h2>{t(lang,"related_stories")}</h2></div>'
          f'<div class="story-grid">{related}</div></div></section>'
          '<section class="stories" style="padding-top:clamp(40px,6vw,80px)"><div class="wrap"><div class="section-head reveal">'
          f'<div class="kicker" data-n="{t(lang,"more_guides")}"><span class="line"></span></div><h2>{t(lang,"more_guides")}</h2></div>'
          f'<div class="story-grid">{more}</div></div></section>'
          '<section class="cta"><div class="wrap row reveal"><div>'
          f'<div class="kicker" data-n="{t(lang,"cta_k")}"><span class="line"></span></div><h2 style="margin-top:20px">{t(lang,"cta_h")}</h2></div>'
          f'<a href="{u(P,lang,"get-in-touch/")}" class="btn light">{t(lang,"start_planning")}</a></div></section>'
          +footer(lang,rel))
        write(lang,rel,head(lang,rel,g['title'][lang]+' — Mountain Elopement',g['excerpt'][lang])+body+scripts(P))

def all_rels():
    rels=['','how-to-elope-in-the-europe-mountains/','stories-elopement-mountain/','our-packages/','our-team/','get-in-touch/','imprint/','privacy-policy/']
    rels+=['portfolio-item/'+s[1]+'/' for s in STORIES]
    rels+=['portfolio-category/'+c+'/' for c in CATS]
    rels+=['how-to-elope-in-the-europe-mountains/'+g['slug']+'/' for g in GUIDES]
    return rels

def build_sitemap():
    out=['<?xml version="1.0" encoding="UTF-8"?>',
         '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    for rel in all_rels():
        for lang in LANGS:
            out.append('<url>')
            out.append(f'<loc>{DOMAIN}/{lbase(lang)}{rel}</loc>')
            for L in LANGS:
                out.append(f'<xhtml:link rel="alternate" hreflang="{L}" href="{DOMAIN}/{lbase(L)}{rel}"/>')
            out.append(f'<xhtml:link rel="alternate" hreflang="x-default" href="{DOMAIN}/{rel}"/>')
            out.append('</url>')
    out.append('</urlset>')
    open(os.path.join(ROOT,'sitemap.xml'),'w').write('\n'.join(out))

def build_robots():
    open(os.path.join(ROOT,'robots.txt'),'w').write(f'User-agent: *\nAllow: /\n\nSitemap: {DOMAIN}/sitemap.xml\n')

def build_410():
    # Root-level 410 body served by Netlify for retired URLs (e.g. old proofing gallery).
    # noindex, no canonical/hreflang — it is a utility Gone page, not a real content page.
    head=('<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">'
        '<meta name="viewport" content="width=device-width, initial-scale=1">'
        '<title>Page no longer available &mdash; Mountain Elopement</title>'
        '<meta name="robots" content="noindex">'
        '<link rel="icon" type="image/png" href="favicon.png"><link rel="apple-touch-icon" href="apple-touch-icon.png">'
        f'{GTM_HEAD}{FONTS}<link rel="stylesheet" href="css/style.css"></head><body>{GTM_BODY}')
    body=(nav('en','','')+
        '<div class="page-plain"><div class="wrap">'
        '<div class="kicker" data-n="410"><span class="line"></span></div>'
        '<h1>This page no longer exists</h1>'
        '<p class="lead">The page you were looking for has been removed &mdash; it may have been a private client gallery that is no longer available.</p>'
        '<p style="margin-top:2em"><a href="/" class="arrow-link">&larr; Back to home</a></p>'
        '</div></div>'
        +footer('en','')+scripts(''))
    open(os.path.join(ROOT,'410.html'),'w').write(head+body)

# ---- merge Italian into all structures (after every dict is defined) ----
for k,v in IT_NAV.items(): T['nav'][k]['it']=v
for k,v in IT.items(): T[k]['it']=v
for k,v in IT_LBL.items(): LBL[k]['it']=v
for k,v in IT_CATS.items(): CATS[k]['it']=v
for s in STORIES: s[4]['it']=IT_ST[s[1]]
for k,v in IT_TITLES.items(): TITLES[k]['it']=v
for k,v in IT_DESC.items(): DESC[k]['it']=v
for g in GUIDES:
    ig=IT_GUIDES[g['slug']]
    g['title']['it']=ig['title']; g['excerpt']['it']=ig['excerpt']; g['intro']['it']=ig['intro']
    for i,sec in enumerate(g['sec']):
        sec['h']['it']=ig['sec'][i][0]; sec['p']['it']=ig['sec'][i][1]
for slug,ex in GUIDE_EXTRA.items():
    ie=IT_EX[slug]
    for i,(lk,val) in enumerate(ex['facts']): val['it']=ie['facts'][i]
    ex['sec4']['h']['it']=ie['sec4'][0]; ex['sec4']['p']['it']=ie['sec4'][1]
    ex['tips']['it']=ie['tips']

for lang in LANGS:
    build_home(lang); build_howto(lang); build_stories(lang); build_categories(lang)
    build_portfolio(lang); build_packages(lang); build_team(lang); build_contact(lang); build_legal(lang)
    build_thankyou(lang); build_guides(lang)
build_sitemap(); build_robots(); build_410()
print('ALL DONE', LANGS)
