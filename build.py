#!/usr/bin/env python3
# Multilingual generator (EN root, /de/, /es/) mirroring the live URL structure.
import os, json, re, html as _html
ROOT = os.path.dirname(os.path.abspath(__file__))
DOMAIN = 'https://mountain-elopement.com'

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
P_MUA  = ('Viki Aichner', 'https://www.vikiaichner.com/de/')
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
 'booking':{'en':'Now booking 2026 &middot; 2027 dates','de':'Buchbar 2026 &middot; Termine 2027','es':'Reservas 2026 &middot; fechas 2027'},
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
 'tm_d1':{'en':'Our planning partner in the Dolomites &mdash; logistics, permits, accommodation and every detail handled on the ground, so you can simply be present.',
          'de':'Unser Planungspartner in den Dolomiten &mdash; Logistik, Genehmigungen, Unterkunft und jedes Detail vor Ort, damit ihr einfach nur da sein könnt.',
          'es':'Nuestro socio de planificación en los Dolomitas &mdash; logística, permisos, alojamiento y cada detalle sobre el terreno, para que solo tengáis que estar presentes.'},
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
 # how to
 'ht_k':{'en':'Field Guide','de':'Ratgeber','es':'Guía'},
 'ht_h1':{'en':'How to Elope in Europe','de':'Elopement in den<br>europäischen Bergen','es':'Cómo fugarse en<br>las montañas de Europa'},
 'ht_s1k':{'en':'Where to begin','de':'Wo ihr beginnt','es':'Por dónde empezar'},
 'ht_s1h':{'en':'Blend adventure<br>and romance','de':'Abenteuer und<br>Romantik verbinden','es':'Aventura y<br>romance unidos'},
 'ht_s1p1':{'en':'Curious about designing an elopement that seamlessly blends adventure and romance in the breathtaking Dolomites? Our expertise lies in curating unforgettable mountain elopements tailored to your unique vision and preferences.',
            'de':'Neugierig auf ein Elopement, das Abenteuer und Romantik in den atemberaubenden Dolomiten vereint? Unsere Stärke ist es, unvergessliche Berghochzeiten ganz nach eurer Vision zu gestalten.',
            'es':'Imagináis un elopement que una aventura y romance en los impresionantes Dolomitas. Nuestra especialidad es crear elopements de montaña inolvidables, hechos a la medida de vuestra visión.'},
 'ht_s1p2':{'en':'We begin by helping you select the perfect mountain location &mdash; considering accessibility, scenery, and the mood you desire. Whether you dream of exchanging vows on a secluded peak or beside a tranquil alpine lake, every detail is shaped around the two of you.',
            'de':'Wir beginnen damit, den perfekten Ort für euch zu finden &mdash; nach Erreichbarkeit, Landschaft und Stimmung. Ob Gipfel oder stiller Bergsee, jedes Detail dreht sich um euch beide.',
            'es':'Empezamos ayudándoos a elegir el lugar perfecto &mdash; según accesibilidad, paisaje y ambiente. Ya soñéis con daros el sí en una cumbre apartada o junto a un lago alpino, cada detalle gira en torno a vosotros dos.'},
 'ht_s1p3':{'en':f'When the day calls for more hands, we work with a trusted circle: on-the-ground planning by <a class="partner-inline" href="{P_PLAN[1]}" target="_blank" rel="noopener">Dolomites Wedding Planner</a>, photography by <a class="partner-inline" href="https://hochzeitsfotograf.tirol" target="_blank" rel="noopener">Blitzkneisser</a> and cinematic coverage by <a class="partner-inline" href="{P_FILM[1]}" target="_blank" rel="noopener">No Matter The Weather</a>.',
            'de':f'Wenn der Tag mehr Hände braucht, arbeiten wir mit einem festen Kreis: Planung vor Ort durch <a class="partner-inline" href="{P_PLAN[1]}" target="_blank" rel="noopener">Dolomites Wedding Planner</a>, Fotografie durch <a class="partner-inline" href="https://hochzeitsfotograf.tirol" target="_blank" rel="noopener">Blitzkneisser</a> und Film durch <a class="partner-inline" href="{P_FILM[1]}" target="_blank" rel="noopener">No Matter The Weather</a>.',
            'es':f'Cuando el día pide más manos, trabajamos con un círculo de confianza: planificación sobre el terreno por <a class="partner-inline" href="{P_PLAN[1]}" target="_blank" rel="noopener">Dolomites Wedding Planner</a>, fotografía por <a class="partner-inline" href="https://hochzeitsfotograf.tirol" target="_blank" rel="noopener">Blitzkneisser</a> y film por <a class="partner-inline" href="{P_FILM[1]}" target="_blank" rel="noopener">No Matter The Weather</a>.'},
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
 'tp_fp1':{'en':'We are a small, local team at home in the Dolomites and the Alps &mdash; planner Jlenia, photographer Andreas and filmmaker Stefanie. For years we have guided couples to quiet summits and hidden lakes, capturing the day exactly as it feels &mdash; unposed, unhurried, real.',
           'de':'Wir sind ein kleines, lokales Team, zu Hause in den Dolomiten/Alpen &mdash; Plannerin Jlenia, Fotograf Andreas und Filmerin Stefanie. Seit Jahren führen wir Paare zu stillen Gipfeln und versteckten Seen und halten den Tag genau so fest, wie er sich anfühlt &mdash; ungestellt, unhektisch, echt.',
           'es':'Somos un equipo pequeño y local, en casa en los Dolomitas y los Alpes &mdash; la planner Jlenia, el fotógrafo Andreas y la filmmaker Stefanie. Durante años hemos guiado a parejas hasta cumbres silenciosas y lagos escondidos, capturando el día tal como se siente &mdash; sin poses, sin prisas, real.'},
 'tp_fp2':{'en':'Between us we photograph, film and plan your entire day &mdash; and where it makes your day even better, we bring in trusted partners like hair &amp; make-up, below.',
           'de':'Gemeinsam fotografieren, filmen und planen wir euren ganzen Tag &mdash; und wo es euren Tag noch schöner macht, holen wir vertraute Partner wie Hair &amp; Make-up dazu, siehe unten.',
           'es':'Entre nosotros fotografiamos, filmamos y planificamos todo vuestro día &mdash; y donde lo mejora aún más, sumamos socios de confianza como peluquería y maquillaje, abajo.'},
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
 (5,'hiking-elopement-lagazuoi-dolomites','s05',['dolomites','elopement','mountain'],{'en':'Hiking Elopement at Lagazuoi, Dolomites','de':'Wander-Hochzeit am Lagazuoi, Dolomiten','es':'Boda de senderismo en el Lagazuoi, Dolomitas'}),
 (6,'pizza-elopement-at-tre-cime-cadini-di-misurina','s06',['dolomites','elopement','mountain'],{'en':'Pizza Elopement at Tre Cime','de':'Pizza-Hochzeit an den Drei Zinnen','es':'Boda con pizza en las Tre Cime'}),
 (7,'mountain-elopement-dolomiten','s07',['dolomites','elopement','mountain'],{'en':'Dolomites Elopement with Three Locations','de':'Dolomiten-Hochzeit an drei Orten','es':'Boda en los Dolomitas en tres lugares'}),
 (8,'sunrise-dolomites-elopement','s08',['dolomites','elopement','mountain'],{'en':'Sunrise in the Dolomites','de':'Sonnenaufgang in den Dolomiten','es':'Amanecer en los Dolomitas'}),
 (9,'official-married-in-the-alps','s09',['elopement','mountain'],{'en':'Official Elopement on Top of Tyrol','de':'Standesamtlich heiraten auf Tirols Gipfel','es':'Boda oficial en la cima del Tirol'}),
 (10,'ultimate-italian-elopement','s10',['elopement'],{'en':'An Elopement Over Three Days','de':'Eine Hochzeit über drei Tage','es':'Una boda de tres días'}),
 (11,'adventure-helicopter-elopement-dolomites','s11',['elopement','dolomites'],{'en':'Adventure Helicopter Elopement in the Dolomites','de':'Abenteuer-Hubschrauber-Hochzeit in den Dolomiten','es':'Boda de aventura en helicóptero en los Dolomitas'}),
 (12,'lake-elopement-tyrol-mountains','s12',['elopement','lake'],{'en':'Elopement at the Lake','de':'Hochzeit am See','es':'Boda junto al lago'}),
 (13,'a-journey-of-love-and-adventure','s13',['couple','engagement'],{'en':'A Journey of Love on Top of Innsbruck','de':'Eine Reise der Liebe über Innsbruck','es':'Un viaje de amor sobre Innsbruck'}),
 (14,'couple-shoot-photo','s14',['couple'],{'en':'Couple Shoot in the Autumn','de':'Paar-Shooting im Herbst','es':'Sesión de pareja en otoño'}),
 (15,'sunset-elopement-tyrol','s15',['elopement','mountain'],{'en':'Mountain-Top Sunset Elopement','de':'Sonnenuntergangs-Hochzeit am Gipfel','es':'Boda al atardecer en la cumbre'}),
 (16,'intimate-lake-eibsee-elopement','s16',['elopement','lake','mountain'],{'en':'Intimate Lake Eibsee Elopement','de':'Intime Hochzeit am Eibsee','es':'Boda íntima en el lago Eibsee'}),
 (17,'lago-di-braies-elopement','s17',['elopement','lake'],{'en':'Lago di Braies Elopement','de':'Hochzeit am Pragser Wildsee','es':'Boda en el Lago di Braies'}),
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
  ]},
 {'slug':'how-to-plan-your-elopement','img':'s01',
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
}

# ================= ITALIAN OVERLAY =================
IT_NAV={'welcome':'Inizio','howto':'Guida','stories':'Storie','packages':'Prezzi','team':'Team','contact':'Contatti'}
IT={
 'ty_k':'Richiesta ricevuta','ty_h':'Grazie',
 'ty_p':'Abbiamo ricevuto il vostro messaggio e vi risponderemo entro 48 ore.',
 'ty_home':'Torna alla home',
 'booking':'Prenotazioni 2026 &middot; date 2027','booking_link':'su richiesta',
 'f_tag':'Fotografia e pianificazione editoriale di elopement nelle Dolomiti e nelle Alpi.',
 'f_explore':'Esplora','f_team':'Il nostro team','f_role_photo':'Foto','f_role_plan':'Pianificazione','f_role_film':'Film','f_role_mua':'Trucco',
 'f_imprint':'Note legali','f_privacy':'Privacy','view_all':'Tutte le storie','start_planning':'Iniziamo a pianificare',
 'get_in_touch':'Contattaci','visit':'Visita','request':'Richiedi','tm_kick':'Il Dream Team','tm_over':'Dietro il vostro giorno',
 'tm_h':'Il team dietro<br>il vostro elopement','tm_r1':'Pianificazione e coordinamento','tm_r2':'Film di elopement','tm_r3':'Trucco e acconciatura',
 'tm_d1':'Il nostro partner di pianificazione nelle Dolomiti &mdash; logistica, permessi, alloggio e ogni dettaglio sul posto, così potete semplicemente esserci.',
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
 'ht_k':'Guida','ht_h1':'Elopement nelle<br>montagne d’Europa','ht_s1k':'Da dove iniziare','ht_s1h':'Unire avventura<br>e romanticismo',
 'ht_s1p1':'Curiosi di progettare un elopement che unisca avventura e romanticismo nelle splendide Dolomiti? La nostra specialità è creare elopement di montagna indimenticabili, su misura per la vostra visione.',
 'ht_s1p2':'Iniziamo aiutandovi a scegliere la location perfetta &mdash; considerando accessibilità, paesaggio e atmosfera desiderata. Che sogniate di scambiarvi le promesse su una vetta appartata o in riva a un lago alpino, ogni dettaglio ruota attorno a voi due.',
 'ht_s1p3':f'Quando il giorno richiede più mani, lavoriamo con una cerchia fidata: pianificazione sul posto di <a class="partner-inline" href="{P_PLAN[1]}" target="_blank" rel="noopener">Dolomites Wedding Planner</a>, fotografia di <a class="partner-inline" href="https://hochzeitsfotograf.tirol" target="_blank" rel="noopener">Blitzkneisser</a> e riprese cinematografiche di <a class="partner-inline" href="{P_FILM[1]}" target="_blank" rel="noopener">No Matter The Weather</a>.',
 'ht_cap':'Un mattino silenzioso sopra il limite del bosco.','ht_e_k':'L’essenziale','ht_e_h':'Cosa considerare',
 'ht_step1t':'Scegliere la location','ht_step1p':'Vetta, lago, prato o cresta &mdash; scegliamo lo scenario in base alla vostra visione, alla stagione e a quanto volete camminare.',
 'ht_step2t':'Pianificare il giorno','ht_step2p':'Un programma rilassato, la luce migliore, un piano flessibile per il meteo e tutta la logistica &mdash; trasferimenti, fiori, trucco e acconciatura.',
 'ht_step3t':'Le vostre promesse','ht_step3p':'Promesse personali, un celebrante o una cerimonia civile opzionale, e una fotografia che cattura tutto esattamente come si è sentito.',
 'ht_ready':'Iniziamo','ht_cta_h':'Iniziamo a pianificare<br>la vostra fuga in montagna',
 'st_k':'L’archivio','st_h':'Storie','st_lead':'Uno sguardo alle avventure che abbiamo avuto l’onore di immortalare &mdash; promesse in vetta, la prima luce sulle creste e momenti di quiete sopra le nuvole.',
 'st_cta_k':'La vostra storia','st_cta_h':'La prossima<br>sarà la vostra?','cat_k':'Categoria','cat_lead':'Storie di elopement nella categoria <em>{x}</em>.',
 'pi_lead':'Un solo giorno, dall’inizio alla fine &mdash; la salita, la luce, il sereno scambio delle promesse e il lungo cammino di ritorno.',
 'pi_p':'Ecco il loro mattino sopra le nuvole, esattamente come si è svolto.','pi_your':'Lo sognate anche voi?','pi_cta_h':'Troviamo<br>la vostra vetta',
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
 'tp_fp1':'Siamo un piccolo team locale, a casa nelle Dolomiti e nelle Alpi &mdash; la planner Jlenia, il fotografo Andreas e la filmmaker Stefanie. Da anni accompagniamo le coppie verso vette silenziose e laghi nascosti, catturando il giorno esattamente come si sente &mdash; senza pose, senza fretta, autentico.',
 'tp_fp2':'Insieme fotografiamo, filmiamo e pianifichiamo tutta la vostra giornata &mdash; e dove la rende ancora più bella, coinvolgiamo partner fidati come trucco e acconciatura, qui sotto.',
 'tp_hello':'Salutateci &rarr;','tp_cta_k':'Un team','tp_cta_h':'Tutto ciò che serve,<br>da un’unica mano','tp_plan':'Pianificate il vostro giorno',
 'ct_k':'Salutateci','ct_h':'Contatti','ct_lead':'Non vediamo l’ora di ascoltare la vostra storia! Raccontateci le vostre idee &mdash; e vi aiuteremo a rendere realtà il vostro elopement da sogno.',
 'ct_details':'I vostri dati','ct_name':'Nome','ct_name_ph':'Il vostro nome','ct_email':'Email','ct_date':'Data elopement (circa)','ct_date_ph':'es. giugno 2027',
 'ct_dream':'Cosa sognate?','ct_story':'Raccontateci la vostra storia','ct_story_ph':'Dove, quando e cosa immaginate...','ct_send':'Invia richiesta',
 'ct_note':'Modulo prototipo &mdash; nella versione finale si collega all’email (es. Formspree).','ct_based':'Sede','ct_based_v':'Tirolo e Dolomiti',
 'chips':['Foto','Film','Backdrop','Fiori','Trucco','Elicottero','Escursione','Musica'],
 'lg_k':'Note legali','lg_imprint':'Note legali','lg_privacy':'Informativa privacy','lg_lead':'Segnaposto &mdash; il testo esistente verrà trasferito invariato dal sito attuale.',
 'guides_k':'Guide di pianificazione','guides_h':'Guide per pianificare il tuo elopement','guides_intro':'Guide pratiche e sincere per pianificare un elopement nelle Alpi e nelle Dolomiti.',
 'read_guide':'Leggi la guida','guide_kick':'Guida','more_guides':'Altre guide','map_k':'La regione','map_h':'Dove vi sposerete?','map_hint':'Tocca una regione',
 'map_tyrol':'Tirolo','map_lakes':'Laghi alpini','map_dol':'Dolomiti','cats_k':'Per tema','cats_h':'Esplora per categoria',
 'quick_facts':'In breve','good_to_know':'Buono a sapersi','related_stories':'Elopement reali',
}
IT_LBL={'season':'Periodo migliore','diff':'Difficoltà','reach':'Come arrivare','regions':'Regioni','access':'Accesso','light':'Luce migliore','lead':'Preavviso','guests':'Ospiti','includes':'Include'}
IT_CATS={'couple':'Coppie','dolomites':'Dolomiti','mountain':'Montagna','lake':'Laghi','elopement':'Elopement','engagement':'Fidanzamento'}
IT_ST={'climbing-wedding':'Matrimonio di arrampicata sulle cime delle Dolomiti','sunrise-elopement-in-the-dolomites':'Un magico elopement all’alba nelle Dolomiti','mountain-engagement':'Proposta in vetta &mdash; fidanzamento in montagna','crystal-clear-water-elopement':'Elopement di montagna presso acque cristalline','hiking-elopement-lagazuoi-dolomites':'Elopement in escursione al Lagazuoi, Dolomiti','pizza-elopement-at-tre-cime-cadini-di-misurina':'Elopement con pizza alle Tre Cime','mountain-elopement-dolomiten':'Elopement nelle Dolomiti in tre location','sunrise-dolomites-elopement':'Alba nelle Dolomiti','official-married-in-the-alps':'Matrimonio ufficiale sulla cima del Tirolo','ultimate-italian-elopement':'Un elopement in tre giorni','adventure-helicopter-elopement-dolomites':'Elopement d’avventura in elicottero nelle Dolomiti','lake-elopement-tyrol-mountains':'Elopement al lago','a-journey-of-love-and-adventure':'Un viaggio d’amore sopra Innsbruck','couple-shoot-photo':'Servizio di coppia in autunno','sunset-elopement-tyrol':'Elopement al tramonto in vetta','intimate-lake-eibsee-elopement':'Elopement intimo al lago Eibsee','lago-di-braies-elopement':'Elopement al Lago di Braies'}
IT_TITLES={'home':'Mountain Elopement — Dove l’avventura incontra il romanticismo','howto':'Elopement nelle montagne d’Europa — Mountain Elopement','stories':'Storie — Mountain Elopement','packages':'Prezzi — Mountain Elopement','team':'Il nostro team e i partner — Mountain Elopement','contact':'Contatti — Mountain Elopement','thankyou':'Grazie per la vostra richiesta — Mountain Elopement'}
IT_DESC={'home':'Fotografia e pianificazione editoriale di elopement nelle Dolomiti e nelle Alpi.','howto':'Una guida per il vostro elopement nelle Dolomiti e nelle Alpi.','stories':'Storie di elopement di montagna nelle Dolomiti e nelle Alpi.','packages':'Pacchetti elopement: fotografia, pianificazione, film, fiori e trucco.','team':'Il team dietro il vostro elopement — fotografia, pianificazione, film e trucco.','contact':'Raccontateci la vostra storia. Fotografia e pianificazione di elopement nelle Dolomiti e nelle Alpi.','thankyou':'Grazie — abbiamo ricevuto la vostra richiesta.'}
IT_GUIDES={
 'dolomites-elopement-guide':{'title':'Elopement nelle Dolomiti','excerpt':'Tutto ciò che serve per sposarvi tra le cime più belle d’Italia.','intro':'Le Dolomiti sono uno dei luoghi più mozzafiato d’Europa per un elopement &mdash; cime drammatiche, laghi turchesi e una luce che tinge la roccia di rosa all’alba. Ecco come rendere il vostro giorno qui semplice.','sec':[('Periodo migliore','Da fine giugno a settembre il tempo è stabile e i rifugi aperti. Per meno folla e larici dorati, pianificate a fine settembre.'),('Dove scambiarvi le promesse','Dalle creste del Seceda alle rive del Lago di Braies e alle Tre Cime, vi aiutiamo a scegliere un luogo adatto alla vostra forma fisica e alla vostra visione.'),('Renderlo ufficiale','In Italia potete sposarvi legalmente con qualche pratica in anticipo, oppure celebrare una cerimonia simbolica e completare la parte legale a casa. Vi indichiamo la strada giusta.')]},
 'elope-in-austria':{'title':'Elopement in Austria e Tirolo','excerpt':'Laghi alpini, alte creste e un matrimonio legale semplice.','intro':'Il Tirolo è casa nostra. Dalle cime sopra Innsbruck ai laghi nascosti, l’Austria rende l’elopement semplice &mdash; anche dal punto di vista legale.','sec':[('Matrimonio legale in Austria','L’Austria consente cerimonie ufficiali in municipio e, in alcune regioni, in splendide location all’aperto. Coordiniamo appuntamento e pratiche.'),('Location migliori','La Nordkette sopra Innsbruck, la Zillertal e innumerevoli laghi alpini sono facilmente raggiungibili.'),('Come arrivare','Innsbruck ha un proprio aeroporto e collegamenti rapidi con Monaco e Venezia, il che rende il Tirolo una delle regioni alpine più accessibili.')]},
 'best-alps-elopement-locations':{'title':'Le migliori location per elopement nelle Alpi','excerpt':'Le nostre vette, laghi e prati preferiti per un giorno indimenticabile.','intro':'Dopo anni in montagna, questi sono i luoghi in cui torniamo di continuo &mdash; ognuno con il proprio carattere e la propria luce.','sec':[('Per gli amanti delle vette','Alte creste e cime per le coppie che cercano la fatica &mdash; e la ricompensa &mdash; di stare in cima.'),('Per gli amanti dell’acqua','Laghi alpini turchesi come Braies, Eibsee e specchi d’acqua tirolesi nascosti per mattine calme e immobili.'),('Per chi ama la calma','Prati dolci e punti panoramici raggiungibili in funivia, quando preferite non camminare troppo.')]},
 'how-to-plan-your-elopement':{'title':'Come pianificare il vostro elopement di montagna','excerpt':'Una tabella di marcia semplice e senza stress, dall’idea al “sì”.','intro':'Pianificare un elopement è molto più semplice di un grande matrimonio &mdash; ma poche decisioni iniziali fanno scorrere tutto. Ecco la versione breve.','sec':[('1 · Prima la sensazione, poi il luogo','Volete avventura e fatica, o calma e semplicità? Questa risposta ci indica la regione e la location giuste.'),('2 · Scegliete stagione e periodo','Inseriamo un margine per il meteo, per poter spostare il vostro giorno di qualche ora o di un giorno secondo le condizioni.'),('3 · Al resto pensiamo noi','Permessi, programma, fiori, trucco e acconciatura, trasferimenti e la parte legale &mdash; tutto gestito con i nostri partner.')]},
}
IT_EX={
 'dolomites-elopement-guide':{'facts':['Giu&ndash;Set','Facile&ndash;Impegnativo','Venezia / Innsbruck &middot; 2&ndash;3 h'],'sec4':('Alba o tramonto?','L’alba significa solitudine e luce morbida con una partenza prima dell’alba; il tramonto è più comodo ma più affollato. Vi aiutiamo a scegliere ciò che fa per voi.'),'tips':['Prenotate presto i rifugi per accedere all’alba.','I larici brillano di più a fine settembre.','Tenete una data flessibile in base al meteo.']},
 'elope-in-austria':{'facts':['Mag&ndash;Ott','Facile&ndash;Moderato','Aeroporto di Innsbruck'],'sec4':('Cerimonia simbolica o legale?','Sposatevi ufficialmente a casa e celebrate una cerimonia simbolica in montagna, oppure completate il matrimonio legale in Austria &mdash; entrambe le opzioni funzionano splendidamente.'),'tips':['L’aeroporto di Innsbruck accorcia il viaggio.','Gli appuntamenti in municipio si riempiono in estate.','Portate abiti a strati &mdash; il meteo di montagna cambia in fretta.']},
 'best-alps-elopement-locations':{'facts':['Dolomiti e Tirolo','Escursione o funivia','Alba'],'sec4':('Quanto camminerete?','Da passeggiate di cinque minuti a vette di un’intera giornata &mdash; adattiamo lo sforzo al vostro comfort, alla forma fisica e alle calzature.'),'tips':['Le funivie regalano grandi panorami con poco sforzo.','I laghi sono più calmi alla prima luce.','Chiedeteci dei luoghi senza permesso.']},
 'how-to-plan-your-elopement':{'facts':['3&ndash;9 mesi','0&ndash;20','Foto &middot; Film &middot; Pianificazione'],'sec4':('Con quanto anticipo prenotare','Le date estive più richieste si riempiono con 6&ndash;12 mesi di anticipo; la bassa stagione è spesso possibile con meno preavviso.'),'tips':['Decidete la sensazione prima del luogo.','Inserite un giorno di margine per il meteo.','Lasciate a noi permessi e fornitori.']},
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
        f'<a class="brand" href="{u(P,lang,"")}"><img class="brand-mark" src="{P}img/logo/mark-dark.png" alt="Mountain Elopement logo"><span class="brand-word">Mountain<span>&middot;</span>Elopement</span></a>'
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
        +card(t(lang,'tm_r2'),NAME_FILM,P_FILM[0],P_FILM[1],t(lang,'tm_d2'))
        +card(t(lang,'tm_r3'),P_MUA[0],t(lang,'visit'),P_MUA[1],t(lang,'tm_d3'))
        +'</div></div></section>')

def footer(lang,rel):
    P=prefix(lang,rel)
    return ('<footer><div class="wrap"><div class="cols">'
      f'<div><div class="fbrand"><img src="{P}img/logo/mark-light.png" alt="Mountain Elopement logo"><span class="fword">Mountain<span>&middot;</span>Elopement</span></div>'
      f'<p>{t(lang,"f_tag")}</p></div>'
      f'<div><h5>{t(lang,"f_explore")}</h5><ul>'
      f'<li><a href="{u(P,lang,"how-to-elope-in-the-europe-mountains/")}">{T["nav"]["howto"][lang]}</a></li>'
      f'<li><a href="{u(P,lang,"stories-elopement-mountain/")}">{T["nav"]["stories"][lang]}</a></li>'
      f'<li><a href="{u(P,lang,"our-packages/")}">{T["nav"]["packages"][lang]}</a></li>'
      f'<li><a href="{u(P,lang,"get-in-touch/")}">{T["nav"]["contact"][lang]}</a></li></ul></div>'
      f'<div><h5>{t(lang,"f_team")}</h5><ul>'
      f'<li><a href="https://blitzkneisser.com" target="_blank" rel="noopener">{t(lang,"f_role_photo")} &middot; Blitzkneisser</a></li>'
      f'<li><a href="{P_PLAN[1]}" target="_blank" rel="noopener">{t(lang,"f_role_plan")} &middot; Dolomites Wedding Planner</a></li>'
      f'<li><a href="{P_FILM[1]}" target="_blank" rel="noopener">{t(lang,"f_role_film")} &middot; No Matter The Weather</a></li>'
      '<li><a href="https://www.instagram.com/mountainelopement/" target="_blank" rel="noopener">Instagram</a></li></ul></div></div>'
      f'<div class="fine"><span>&copy; 2026 mountain-elopement by blitzkneisser.com</span>'
      f'<span><a href="{u(P,lang,"imprint/")}">{t(lang,"f_imprint")}</a> &middot; <a href="{u(P,lang,"privacy-policy/")}">{t(lang,"f_privacy")}</a> &middot; Prototype</span></div></div></footer>')

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

LB_JS=("<script>var gal=document.getElementById('gal');var imgs=[].slice.call(gal.querySelectorAll('img'));"
 "var srcs=imgs.map(function(x){return x.getAttribute('src');});var N=srcs.length;"
 "var lb=document.getElementById('lb'),lbimg=document.getElementById('lbimg'),cur=0;"
 "function open(i){cur=i;lbimg.src=srcs[i];lb.classList.add('open');}function close(){lb.classList.remove('open');}"
 "imgs.forEach(function(im,i){im.addEventListener('click',function(){open(i);});});"
 "document.getElementById('lbx').onclick=close;lb.addEventListener('click',function(e){if(e.target===lb)close();});"
 "document.getElementById('lbn').onclick=function(e){e.stopPropagation();open((cur+1)%N);};"
 "document.getElementById('lbp').onclick=function(e){e.stopPropagation();open((cur-1+N)%N);};"
 "addEventListener('keydown',function(e){if(!lb.classList.contains('open'))return;"
 "if(e.key==='Escape')close();if(e.key==='ArrowRight')open((cur+1)%N);if(e.key==='ArrowLeft')open((cur-1+N)%N);});</script>")

def gallery_html(lang,P,slug,alt):
    d=os.path.join(ROOT,'img','gallery',slug)
    imgs=sorted(os.listdir(d)) if os.path.isdir(d) else []
    if not imgs:  # fallback to shared placeholder set
        imgs=[f'../g{i:02d}.webp' for i in range(1,13)]
        return '<div class="gallery" id="gal">'+''.join(f'<img src="{P}img/gallery/{fn.split("/")[-1]}" loading="lazy" alt="{alt}">' for fn in imgs)+'</div>'
    return '<div class="gallery" id="gal">'+''.join(f'<img src="{P}img/gallery/{slug}/{fn}" loading="lazy" alt="{alt}">' for fn in imgs)+'</div>'

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
      f'<div class="meta-strip"><div class="wide"><span>{t(lang,"ms1")}</span><span>{t(lang,"ms2")}</span>'
      f'<span>{t(lang,"ms3")}</span><span>{t(lang,"ms4")}</span></div></div>'
      '<section><div class="wrap feature"><div class="body reveal">'
      f'<div class="kicker" data-n="01">{t(lang,"mission_k")}<span class="line"></span></div><h2>{t(lang,"mission_h")}</h2>'
      f'<p class="lead">{t(lang,"mission_lead")}</p><p class="dropcap">{t(lang,"mission_p1")}</p><p>{t(lang,"mission_p2")}</p>'
      f'<a href="{u(P,lang,"how-to-elope-in-the-europe-mountains/")}" class="arrow-link">{t(lang,"mission_link")}</a></div>'
      f'<div class="media reveal"><img src="{P}img/story/mission.webp" alt="Elopement"><div class="caption">{t(lang,"cap_seceda")}</div></div></div></section>'
      '<hr class="hr"><section><div class="wrap"><div class="section-head reveal">'
      f'<div class="kicker" data-n="{t(lang,"diff_k")}"><span class="line"></span></div><h2>{t(lang,"diff_h")}</h2></div>'
      '<div class="pillars reveal">'
      f'<div class="pillar"><h3>{t(lang,"diff1_h")}</h3><p>{t(lang,"diff1_p")}</p></div>'
      f'<div class="pillar"><h3>{t(lang,"diff2_h")}</h3><p>{t(lang,"diff2_p")}</p></div>'
      f'<div class="pillar"><h3>{t(lang,"diff3_h")}</h3><p>{t(lang,"diff3_p")}</p></div>'
      f'<div class="pillar"><h3>{t(lang,"diff4_h")}</h3><p>{t(lang,"diff4_p")}</p></div></div>'
      '<div class="badges reveal" style="margin-top:44px">'
      f'<a class="badge" href="https://wayupnorth.co/2024-wun-awards-photo-contest-winners/" target="_blank" rel="noopener">'
      f'<img src="{P}img/badges/wun-2024-400.png" srcset="{P}img/badges/wun-2024-400.png 400w, {P}img/badges/wun-2024.png 800w" sizes="72px" alt="Way Up North Awards 2024 &ndash; Winner Best Epic Portrait" width="400" height="400" loading="lazy">'
      f'<span class="badge-txt"><span class="badge-eyebrow">{t(lang,"award_lbl")}</span><strong>Way Up North Awards 2024</strong><span class="badge-sub">Winner &ndash; Best Epic Portrait</span></span></a>'
      f'<a class="badge" href="https://rangefinderonline.com/news-features/photo-of-the-day/ankle-deep-in-beauty/" target="_blank" rel="noopener">'
      f'<span class="badge-txt"><span class="badge-eyebrow">{t(lang,"pub_lbl")}</span><strong>Rangefinder Magazine</strong><span class="badge-sub">Rf Photo of the Day &ndash; Lago di Braies</span></span></a>'
      '</div></div></section>'
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
      '<section class="cta"><div class="wrap row reveal"><div>'
      f'<div class="kicker" data-n="04">{t(lang,"cta_k")}<span class="line"></span></div><h2 style="margin-top:20px">{t(lang,"cta_h")}</h2></div>'
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
      f'<div class="content"><div class="wrap"><div class="kicker" data-n="{t(lang,"ht_k")}"><span class="line"></span></div><h1>{t(lang,"ht_h1")}</h1></div></div></section>'
      '<section><div class="wrap feature"><div class="body reveal">'
      f'<div class="kicker" data-n="01">{t(lang,"ht_s1k")}<span class="line"></span></div><h2>{t(lang,"ht_s1h")}</h2>'
      f'<p class="dropcap">{t(lang,"ht_s1p1")}</p><p>{t(lang,"ht_s1p2")}</p><p>{t(lang,"ht_s1p3")}</p></div>'
      f'<div class="media reveal"><img src="{P}img/stories/s08.webp" alt="Dolomites"><div class="caption">{t(lang,"ht_cap")}</div></div></div></section>'
      '<hr class="hr"><section><div class="wrap"><div class="section-head reveal">'
      f'<div class="kicker" data-n="02">{t(lang,"ht_e_k")}<span class="line"></span></div><h2>{t(lang,"ht_e_h")}</h2></div>'
      '<div class="story-grid" style="align-items:start">'
      +step('01','ht_step1t','ht_step1p')+step('02','ht_step2t','ht_step2p')+step('03','ht_step3t','ht_step3p')+
      '</div></div></section>'
      '<section class="stories"><div class="wrap"><div class="section-head reveal">'
      f'<div class="kicker" data-n="{t(lang,"guides_k")}"><span class="line"></span></div><h2>{t(lang,"guides_h")}</h2>'
      f'<p style="max-width:640px;color:var(--ink-2);margin:0">{t(lang,"guides_intro")}</p></div>'
      +guide_mosaic(lang,P)+
      '</div></section>'
      +team_section(lang,P)+
      '<section class="cta"><div class="wrap row reveal"><div>'
      f'<div class="kicker" data-n="{t(lang,"ht_ready")}"><span class="line"></span></div><h2 style="margin-top:20px">{t(lang,"ht_cta_h")}</h2></div>'
      f'<a href="{u(P,lang,"get-in-touch/")}" class="btn light">{t(lang,"get_in_touch")}</a></div></section>'
      +footer(lang,rel))
    write(lang,rel,head(lang,rel,TITLES['howto'][lang],DESC['howto'][lang])+body+scripts(P))

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

def build_portfolio(lang):
    for s in STORIES:
        num,slug,img,cats,titles=s
        rel=f'portfolio-item/{slug}/'; P=prefix(lang,rel)
        catlinks=' &middot; '.join(f'<a href="{u(P,lang,"portfolio-category/"+c+"/")}" style="color:inherit">{catname(c,lang)}</a>' for c in cats)
        body=(nav(lang,rel,'stories')+
          f'<section class="page-hero" style="padding:0"><div class="bg" style="background-image:url(\'{P}img/stories/{img}.webp\')"></div>'
          f'<div class="content"><div class="wrap"><div class="kicker" data-n="Story N&deg;{num:02d}"><span class="line"></span></div><h1>{titles[lang]}</h1></div></div></section>'
          f'<div class="page-plain" style="border-top:0"><div class="wrap feature" style="align-items:start;padding-bottom:clamp(30px,4vw,50px)">'
          f'<div class="reveal"><div class="cap" style="margin-bottom:14px">{catlinks}</div><p class="lead" style="margin:0">{t(lang,"pi_lead")}</p></div>'
          f'<div class="reveal"><p style="color:var(--ink-2);font-size:17px;margin:0 0 14px">{t(lang,"pi_p")}</p>'
          f'<p class="small" style="color:var(--ink-2)">{t(lang,"pi_vplan")} <a class="partner-inline" href="{P_PLAN[1]}" target="_blank" rel="noopener">Dolomites Wedding Planner</a> &middot; '
          f'{t(lang,"pi_vfilm")} <a class="partner-inline" href="{P_FILM[1]}" target="_blank" rel="noopener">No Matter The Weather</a> &middot; '
          f'{t(lang,"pi_vmua")} <a class="partner-inline" href="{P_MUA[1]}" target="_blank" rel="noopener">Viki Aichner</a></p></div></div></div>'
          '<section><div class="wide">'+gallery_html(lang,P,slug,titles[lang])+'</div></section>'
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
    def tier(no,label,name,price,items,feat=False):
        cls='tier feat' if feat else 'tier'
        lis=''.join('<li>'+i+'</li>' for i in items)
        lk='margin-top:22px;display:inline-block'+(';border-color:#fff;color:#fff' if feat else '')
        return (f'<div class="{cls}"><div class="no">N&deg;{no} &mdash; {label}</div><div class="name">{name}</div>'
          f'<div class="price">&euro; {price}</div><ul>{lis}</ul>'
          f'<a href="{u(P,lang,"get-in-touch/")}" class="arrow-link" style="{lk}">{t(lang,"request")} &rarr;</a></div>')
    photoword={'en':'Photography','de':'Fotografie','es':'Fotografía','it':'Fotografia'}[lang]
    gr={'en':'Getting ready','de':'Getting Ready','es':'Preparativos','it':'Preparativi'}[lang]
    gropt={'en':'Getting ready (optional)','de':'Getting Ready (optional)','es':'Preparativos (opcional)','it':'Preparativi (opzionale)'}[lang]
    loc={'en':'Location scouting','de':'Location-Scouting','es':'Búsqueda de localización','it':'Sopralluogo location'}[lang]
    concept={'en':'Concept & idea','de':'Konzept & Idee','es':'Concepto e idea','it':'Concept e idea'}[lang]
    flowers={'en':'Flowers · Hair & Make-up','de':'Blumen · Hair & Make-up','es':'Flores · Peluquería y maquillaje','it':'Fiori · Trucco e acconciatura'}[lang]
    locplan={'en':'Location · Organisation & planning','de':'Location · Organisation & Planung','es':'Localización · Organización y planificación','it':'Location · Organizzazione e pianificazione'}[lang]
    fullplan={'en':'Full planning: accommodation, reception, transfers','de':'Komplette Planung: Unterkunft, Empfang, Transfers','es':'Planificación completa: alojamiento, recepción, traslados','it':'Pianificazione completa: alloggio, ricevimento, trasferimenti'}[lang]
    t1=tier('01',t(lang,'pk_l1'),t(lang,'pk_t1'),'5.200',[f'{photoword} (50&ndash;80 {ph})',f'2&ndash;3 {hrs}',loc,concept])
    t2=tier('02',t(lang,'pk_l2'),t(lang,'pk_t2'),'7.400',[f'{photoword} (80&ndash;100 {ph})',f'4&ndash;5 {hrs}',gropt,flowers,locplan],feat=True)
    t3=tier('03',t(lang,'pk_l3'),t(lang,'pk_t3'),'9.800',[f'{photoword} (100&ndash;200 {ph})',f'6&ndash;8 {hrs}',gr,flowers,fullplan])
    def ad(name,price): return f'<div class="addon"><div class="a">{name}</div><div class="p">{price}</div></div>'
    addons=(ad(t(lang,'ad_heli'),'&asymp; &euro; 2.500')
      +ad(f'<a href="{P_FILM[1]}" target="_blank" rel="noopener" style="color:inherit">{t(lang,"ad_film")}</a>','&asymp; &euro; 3.500')
      +ad(t(lang,'ad_civil'),'&asymp; &euro; 1.000')+ad(t(lang,'ad_celeb'),'&asymp; &euro; 1.500')
      +ad(t(lang,'ad_cake'),f'{t(lang,"ad_from")} &euro; 400')+ad(t(lang,'ad_music'),'&asymp; &euro; 600')
      +ad(f'<a href="{P_MUA[1]}" target="_blank" rel="noopener" style="color:inherit">{t(lang,"ad_mua")}</a>',t(lang,'ad_onreq'))
      +ad(t(lang,'ad_backdrop'),'&euro; 600'))
    body=(nav(lang,rel,'packages')+
      f'<div class="page-plain"><div class="wrap"><div class="kicker" data-n="{t(lang,"pk_k")}"><span class="line"></span></div>'
      f'<h1>{t(lang,"pk_h")}</h1><p class="lead">{t(lang,"pk_lead")}</p></div></div>'
      f'<section><div class="wrap"><div class="tiers reveal">{t1}{t2}{t3}</div>'
      f'<p class="lead reveal" style="max-width:760px;margin-top:clamp(40px,5vw,64px)">{t(lang,"pk_note")}</p>'
      f'<div class="section-head reveal" style="margin-top:clamp(40px,6vw,72px)"><div class="kicker" data-n="Add-ons">{t(lang,"pk_addk")}<span class="line"></span></div></div>'
      f'<div class="addons reveal">{addons}</div></div></section>'
      '<section class="band"><div class="wrap quote reveal">'
      f'<div class="kicker" data-n="{t(lang,"pk_band_k")}"><span class="line"></span></div>'
      f'<p style="margin-top:26px">{t(lang,"pk_band_q")}</p><div class="who">Jlenia, Andreas &amp; Stefanie &mdash; Mountain Elopement</div></div></section>'
      '<section class="cta"><div class="wrap row reveal"><div>'
      f'<div class="kicker" data-n="{t(lang,"pk_next")}"><span class="line"></span></div><h2 style="margin-top:20px">{t(lang,"pk_cta_h")}</h2></div>'
      f'<a href="{u(P,lang,"get-in-touch/")}" class="btn light">{t(lang,"pk_req_price")}</a></div></section>'
      +footer(lang,rel))
    write(lang,rel,head(lang,rel,TITLES['packages'][lang],DESC['packages'][lang])+body+scripts(P))

def build_team(lang):
    rel='our-team/'; P=prefix(lang,rel)
    body=(nav(lang,rel,'team')+
      f'<div class="page-plain"><div class="wrap"><div class="kicker" data-n="{t(lang,"tp_k")}"><span class="line"></span></div>'
      f'<h1>{t(lang,"tp_h")}</h1><p class="lead">{t(lang,"tp_lead")}</p></div></div>'
      f'<section><div class="wrap feature"><div class="media reveal"><img id="teamhero" src="{P}{TEAM_HERO[0]}" alt="Jlenia, Andreas and Stefanie in the mountains">'
      '<div class="caption">Jlenia, Andreas &amp; Stefanie.</div></div><div class="body reveal">'
      f'<div class="kicker" data-n="01">{t(lang,"tp_fk")}<span class="line"></span></div><h2>Jlenia, Andreas &amp; Stefanie</h2>'
      f'<p class="lead">{t(lang,"tp_flead")}</p><p class="dropcap">{t(lang,"tp_fp1")}</p><p>{t(lang,"tp_fp2")}</p>'
      f'<a href="{u(P,lang,"get-in-touch/")}" class="arrow-link">{t(lang,"tp_hello")}</a></div></div></section>'
      +team_section(lang,P)+
      '<section><div class="wrap"><div class="section-head reveal">'
      f'<div class="kicker" data-n="{t(lang,"bts_k")}">{t(lang,"bts_over")}<span class="line"></span></div><h2>{t(lang,"bts_h")}</h2></div>'
      '<div class="bts-grid reveal">'
      f'<img src="{P}img/team/bts-roses.webp" alt="The Mountain Elopement team with a couple, alpine meadow" loading="lazy">'
      f'<img src="{P}img/team/bts-meadow.webp" alt="The Mountain Elopement team celebrating with a couple" loading="lazy">'
      f'<img src="{P}img/team/bts-group.webp" alt="The Mountain Elopement team and a couple in the Dolomites" loading="lazy">'
      '</div></div></section>'
      '<section class="cta"><div class="wrap row reveal"><div>'
      f'<div class="kicker" data-n="{t(lang,"tp_cta_k")}"><span class="line"></span></div><h2 style="margin-top:20px">{t(lang,"tp_cta_h")}</h2></div>'
      f'<a href="{u(P,lang,"get-in-touch/")}" class="btn light">{t(lang,"tp_plan")}</a></div></section>'
      +footer(lang,rel))
    hero_js=('<script>(function(){var s=['+','.join("'"+P+h+"'" for h in TEAM_HERO)+
             "];var i=document.getElementById('teamhero');if(i)i.src=s[Math.floor(Math.random()*s.length)];})();</script>")
    write(lang,rel,head(lang,rel,TITLES['team'][lang],DESC['team'][lang])+body+scripts(P,hero_js))

def build_contact(lang):
    rel='get-in-touch/'; P=prefix(lang,rel)
    chips=''.join(f'<span class="chip">{c}</span>' for c in T['chips'][lang])
    extra=("<script>document.getElementById('chips').addEventListener('click',function(e){"
           "if(e.target.classList.contains('chip'))e.target.classList.toggle('on');});</script>")
    body=(nav(lang,rel,'contact')+
      f'<div class="page-plain"><div class="wrap"><div class="kicker" data-n="{t(lang,"ct_k")}"><span class="line"></span></div>'
      f'<h1>{t(lang,"ct_h")}</h1><p class="lead">{t(lang,"ct_lead")}</p></div></div>'
      '<section><div class="wrap contact-grid"><form class="form reveal" onsubmit="return false">'
      f'<div class="kicker" data-n="01" style="margin-bottom:22px">{t(lang,"ct_details")}<span class="line"></span></div>'
      f'<label>{t(lang,"ct_name")}</label><input type="text" placeholder="{t(lang,"ct_name_ph")}">'
      f'<label>{t(lang,"ct_email")}</label><input type="email" placeholder="you@email.com">'
      f'<label>{t(lang,"ct_date")}</label><input type="text" placeholder="{t(lang,"ct_date_ph")}">'
      f'<label>{t(lang,"ct_dream")}</label><div class="chips" id="chips">{chips}</div>'
      f'<label>{t(lang,"ct_story")}</label><textarea rows="5" placeholder="{t(lang,"ct_story_ph")}"></textarea>'
      f'<button class="btn" type="submit">{t(lang,"ct_send")}</button>'
      f'<p class="small" style="margin-top:14px;color:var(--ink-2)">{t(lang,"ct_note")}</p></form>'
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

def guide_mosaic(lang,P):
    cls=['m-tile m-w','m-tile m-n','m-tile m-n','m-tile m-w']
    tiles=''
    for i,g in enumerate(GUIDES):
        c=cls[i] if i<len(cls) else 'm-tile'
        href=u(P,lang,'how-to-elope-in-the-europe-mountains/'+g['slug']+'/')
        tiles+=(f'<a class="{c} reveal" href="{href}"><img src="{P}img/stories/{g["img"]}.webp" alt="{g["title"][lang]}">'
                f'<div class="m-cap"><div class="m-cat">{t(lang,"guide_kick")}</div><h3>{g["title"][lang]}</h3></div></a>')
    return '<div class="mosaic">'+tiles+'</div>'

def build_guides(lang):
    for g in GUIDES:
        ex=GUIDE_EXTRA[g['slug']]
        rel='how-to-elope-in-the-europe-mountains/'+g['slug']+'/'; P=prefix(lang,rel)
        facts='<div class="facts">'+''.join(f'<div class="fct"><div class="fl">{LBL[k][lang]}</div><div class="fv">{val[lang]}</div></div>' for k,val in ex['facts'])+'</div>'
        allsec=g['sec']+[ex['sec4']]
        secs=''
        for s in allsec:
            secs+=(f'<h2 style="font-family:var(--serif);font-weight:400;font-size:clamp(25px,3vw,36px);letter-spacing:-.01em;margin:1.5em 0 .35em">{s["h"][lang]}</h2>'
                   f'<p style="color:var(--ink-2)">{s["p"][lang]}</p>')
        tips='<div class="tips"><h4>'+t(lang,'good_to_know')+'</h4><ul>'+''.join('<li>'+it+'</li>' for it in ex['tips'][lang])+'</ul></div>'
        related=''.join(story_card(lang,P,STORYBY[sl]) for sl in ex['stories'])
        more=''.join(guide_card(lang,P,x) for x in GUIDES if x['slug']!=g['slug'])
        body=(nav(lang,rel,'howto')+
          f'<section class="page-hero" style="padding:0"><div class="bg" style="background-image:url(\'{P}img/stories/{g["img"]}.webp\')"></div>'
          f'<div class="content"><div class="wrap"><div class="kicker" data-n="{t(lang,"guide_kick")}"><span class="line"></span></div><h1>{g["title"][lang]}</h1></div></div></section>'
          '<section><div class="wrap" style="max-width:820px">'
          f'<p class="lead">{g["intro"][lang]}</p>'
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
build_sitemap(); build_robots()
print('ALL DONE', LANGS)
