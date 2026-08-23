-- Data migration from flat JSON files to Cloudflare D1

INSERT OR REPLACE INTO tours (id, slug, nombre, categoria, estado, duracion_dias, duracion_noches, precio_desde, moneda, capacidad_min, capacidad_max, dificultad, temporada, descripcion_corta, descripcion_larga, imagen_hero, imagen_alt, galeria_json, itinerario_json, transporte_json, created_at) VALUES ('3-day-wildlife-quest-machu-wasi', '3-day-wildlife-quest-machu-wasi', '3-Day Wildlife Quest – Machu Wasi', 'wildlife', 'activo', 3, 2, 450, 'USD', 2, 8, 'Fácil', 'Mayo - Octubre (Temporada Seca)', 'Un tour de vida silvestre de 3 días al Parque Nacional Manu, ideal para quienes tienen poco tiempo pero quieren experimentar la Amazonía peruana.', 'Este tour de 3 días es perfecto para quienes quieren experimentar la selva amazónica sin alejarse demasiado. Viajamos en van por el bosque nuboso, descendemos hasta la selva baja y exploramos los ríos en bote buscando caimanes, capybaras y aves exóticas en Machu Wasi.', '/media/1786591103305-pteronura-brasiliensis-zoo-brasilia-01.jpg', '3-Day Wildlife Quest at Machu Wasi – Manu National Park', '[{"url":"assets/media_to_upload/photos/placeholder.jpg","alt":"Wildlife at Machu Wasi"}]', '[{"dia":1,"titulo":"Cusco → Cloud Forest → Machu Wasi Lodge","descripcion":"Departure from Cusco at 6:00 AM. We drive through the stunning cloud forest, stopping at viewpoints along the way. Arrive at Machu Wasi Lodge in the afternoon. Enjoy a welcome dinner and night walk spotting nocturnal wildlife."},{"dia":2,"titulo":"River Safari & Wildlife Walks","descripcion":"Early morning boat safari on the river searching for caimans, capybaras, and birds. Afternoon jungle walks on forest trails with our expert local guide. Evening optional fishing."},{"dia":3,"titulo":"Morning Wildlife → Return to Cusco","descripcion":"Final morning birdwatching session. After breakfast, we begin the return journey to Cusco, arriving in the late afternoon."}]', '["Van privada","Bote"]', '2026-08-23T19:57:54.035Z');
INSERT OR REPLACE INTO tours (id, slug, nombre, categoria, estado, duracion_dias, duracion_noches, precio_desde, moneda, capacidad_min, capacidad_max, dificultad, temporada, descripcion_corta, descripcion_larga, imagen_hero, imagen_alt, galeria_json, itinerario_json, transporte_json, created_at) VALUES ('4-day-wildlife-quest-machu-wasi', '4-day-wildlife-quest-machu-wasi', '4-Day Wildlife Quest – Machu Wasi', 'wildlife', 'activo', 4, 3, 580, 'USD', 2, 8, 'Fácil', 'Todo el año', 'Cuatro días para explorar la selva amazónica en profundidad desde Machu Wasi. Ver caímanes, capybaras, monos y aves de la Amazonía.', 'El tour de 4 días a Machu Wasi ofrece más tiempo en la selva para aumentar las probabilidades de avistar vida silvestre. Con tres noches en el lodge, tenemos tiempo para caminatas de día y de noche, safaris en bote y actividades de kayak.', 'assets/img/hero.png', '4-Day Wildlife Quest at Machu Wasi – Manu National Park', '[]', '[{"dia":1,"titulo":"Cusco → Cloud Forest → Machu Wasi Lodge","descripcion":"Departure from Cusco at 6:00 AM. Drive through the cloud forest with stops at scenic viewpoints. Arrive at the lodge in the afternoon for welcome dinner and night walk."},{"dia":2,"titulo":"River Safari & Jungle Walks","descripcion":"Full day of wildlife activities: morning boat safari, afternoon jungle trails, evening optional piranha fishing."},{"dia":3,"titulo":"Deep Jungle Exploration","descripcion":"Longer hike into the forest to discover hidden oxbow lakes. Kayaking on the river. Sunset watching from the observation platform."},{"dia":4,"titulo":"Morning Birds → Return to Cusco","descripcion":"Final birdwatching session at dawn. Breakfast and return journey to Cusco arriving late afternoon."}]', '["Van privada","Bote"]', '2026-08-23T19:57:54.036Z');
INSERT OR REPLACE INTO tours (id, slug, nombre, categoria, estado, duracion_dias, duracion_noches, precio_desde, moneda, capacidad_min, capacidad_max, dificultad, temporada, descripcion_corta, descripcion_larga, imagen_hero, imagen_alt, galeria_json, itinerario_json, transporte_json, created_at) VALUES ('4-day-wildlife-quest-nuevo-eden', '4-day-wildlife-quest-nuevo-eden', '4-Day Wildlife Quest – Nuevo Eden', 'wildlife', 'activo', 4, 3, 560, 'USD', 2, 8, 'Fácil', 'Todo el año', 'Tour de vida silvestre de 4 días desde el pueblo de Nuevo Eden, hogar de nuestra familia fundadora. Una experiencia profundamente local y auténtica.', 'Nuevo Eden es el pueblo donde creció Moisés, co-fundador de Manu Jungle Forever. Este tour ofrece la experiencia más auténtica con acceso a nuestros propios senderos privados y lodge familiar.', 'assets/img/hero.png', 'Wildlife Quest at Nuevo Eden – Manu National Park', '[]', '[{"dia":1,"titulo":"Cusco → Nuevo Eden Lodge","descripcion":"Early morning departure from Cusco. Scenic drive through the Andes and cloud forest. Arrive at Nuevo Eden and begin with an evening boat trip."},{"dia":2,"titulo":"Wildlife Safari Day","descripcion":"Full day wildlife activities: morning boat safari on the Madre de Dios river, afternoon jungle walks, night walk."},{"dia":3,"titulo":"Village Life & Nature","descripcion":"Visit the community of Nuevo Eden, learn about local traditions, afternoon kayak session, evening wildlife spotting."},{"dia":4,"titulo":"Dawn Birds → Cusco","descripcion":"Sunrise birdwatching, breakfast, return drive to Cusco."}]', '["Van privada","Bote"]', '2026-08-23T19:57:54.036Z');
INSERT OR REPLACE INTO tours (id, slug, nombre, categoria, estado, duracion_dias, duracion_noches, precio_desde, moneda, capacidad_min, capacidad_max, dificultad, temporada, descripcion_corta, descripcion_larga, imagen_hero, imagen_alt, galeria_json, itinerario_json, transporte_json, created_at) VALUES ('5-day-wildlife-quest-nuevo-eden', '5-day-wildlife-quest-nuevo-eden', '5-Day Wildlife Quest – Nuevo Eden', 'wildlife', 'activo', 5, 4, 680, 'USD', 2, 8, 'Moderado', 'Todo el año', 'Cinco días de inmersión total en la selva amazónica desde Nuevo Eden con mayores probabilidades de avistar fauna exótica.', 'El tour de 5 días a Nuevo Eden es nuestra opción más popular para quienes quieren máxima exposición a la vida silvestre con comodidad. Con cuatro noches, exploramos la selva, los ríos y el bosque nuboso en toda su diversidad.', 'assets/img/hero.png', '5-Day Wildlife Quest at Nuevo Eden', '[]', '[{"dia":1,"titulo":"Cusco → Nuevo Eden","descripcion":"Departure from Cusco, cloud forest drive, evening arrival and welcome dinner."},{"dia":2,"titulo":"River Safari & Jungle Walks","descripcion":"Full day of wildlife activities on the river and trails."},{"dia":3,"titulo":"Oxbow Lake & Deep Forest","descripcion":"Boat trip to a hidden oxbow lake. Afternoon hiking in primary rainforest."},{"dia":4,"titulo":"Fishing, Kayak & Night Walk","descripcion":"Fishing for piranhas, kayak session, traditional piranha fishing dinner, night wildlife walk."},{"dia":5,"titulo":"Dawn Walk → Return to Cusco","descripcion":"Early morning bird walk, breakfast, return to Cusco."}]', '["Van privada","Bote"]', '2026-08-23T19:57:54.036Z');
INSERT OR REPLACE INTO tours (id, slug, nombre, categoria, estado, duracion_dias, duracion_noches, precio_desde, moneda, capacidad_min, capacidad_max, dificultad, temporada, descripcion_corta, descripcion_larga, imagen_hero, imagen_alt, galeria_json, itinerario_json, transporte_json, created_at) VALUES ('6-day-wildlife-quest-blanquillo', '6-day-wildlife-quest-blanquillo', '6-Day Wildlife Quest – Blanquillo', 'wildlife', 'activo', 6, 5, 890, 'USD', 2, 8, 'Moderado', 'Todo el año', 'El tour de 6 días a Blanquillo incluye la visita al famoso comedero de arcilla de guacamayos — uno de los espectáculos de vida silvestre más impresionantes del Perú.', 'Blanquillo es famoso por su colpa de guacamayos, donde cientos de guacamayos de colores llegan cada mañana al amanecer. Este tour de 6 días incluye esta experiencia única más 5 noches de exploración intensiva de la selva amazónica.', 'assets/img/hero.png', '6-Day Wildlife Quest – Blanquillo Macaw Clay Lick', '[]', '[{"dia":1,"titulo":"Cusco → Cloud Forest → Nuevo Eden","descripcion":"Early departure, scenic cloud forest drive, afternoon arrival."},{"dia":2,"titulo":"River Wildlife Safari","descripcion":"Full day boat safaris searching for caimans, giant otters and river wildlife."},{"dia":3,"titulo":"Blanquillo Macaw Clay Lick – Dawn","descripcion":"Pre-dawn boat journey to the famous Blanquillo clay lick. Watch hundreds of colorful macaws gather at sunrise."},{"dia":4,"titulo":"Deep Jungle Expedition","descripcion":"Trek into primary rainforest. Night walk to spot nocturnal wildlife."},{"dia":5,"titulo":"Oxbow Lake & Fishing","descripcion":"Visit a remote oxbow lake, piranha fishing, community visit in Nuevo Eden."},{"dia":6,"titulo":"Sunrise Birds → Return to Cusco","descripcion":"Final morning birdwatching, breakfast, return to Cusco."}]', '["Van privada","Bote"]', '2026-08-23T19:57:54.036Z');
INSERT OR REPLACE INTO tours (id, slug, nombre, categoria, estado, duracion_dias, duracion_noches, precio_desde, moneda, capacidad_min, capacidad_max, dificultad, temporada, descripcion_corta, descripcion_larga, imagen_hero, imagen_alt, galeria_json, itinerario_json, transporte_json, created_at) VALUES ('6-day-wildlife-quest-reserved-zone', '6-day-wildlife-quest-reserved-zone', 'Manu Reserved Zone – 6 Days', 'wildlife', 'activo', 6, 5, 1200, 'USD', 2, 8, 'Moderado', 'Abril a Noviembre', 'El tour más exclusivo de Manu Jungle Forever: acceso a la Zona Reservada del Manu donde la vida silvestre es más abundante y el hábitat está pristino.', 'La Zona Reservada del Parque Nacional Manu es una de las áreas más biodiversas del planeta. Este tour de 6 días penetra hasta el corazón de la reserva con permisos especiales para brindar el máximo avistamiento de fauna.', 'assets/img/hero.png', 'Manu National Park Reserved Zone Tour', '[]', '[{"dia":1,"titulo":"Cusco → Cloud Forest","descripcion":"Early departure, overnight in cloud forest lodge."},{"dia":2,"titulo":"Cloud Forest → Manu Zone","descripcion":"Continue journey into the Manu buffer zone. First wildlife sightings."},{"dia":3,"titulo":"Enter the Reserved Zone","descripcion":"Enter the restricted reserved zone. Exceptional wildlife viewing on the river."},{"dia":4,"titulo":"Deep Manu Exploration","descripcion":"Full day in the reserved zone: trails, river safaris, macaw lick."},{"dia":5,"titulo":"Return Journey Begins","descripcion":"Start return, overnight in buffer zone."},{"dia":6,"titulo":"Return to Cusco","descripcion":"Complete return to Cusco."}]', '["Van privada","Bote"]', '2026-08-23T19:57:54.036Z');
INSERT OR REPLACE INTO tours (id, slug, nombre, categoria, estado, duracion_dias, duracion_noches, precio_desde, moneda, capacidad_min, capacidad_max, dificultad, temporada, descripcion_corta, descripcion_larga, imagen_hero, imagen_alt, galeria_json, itinerario_json, transporte_json, created_at) VALUES ('8-day-wildlife-photography-tour', '8-day-wildlife-photography-tour', 'Wildlife Photography Tour – 8 Days', 'wildlife', 'activo', 8, 7, 1450, 'USD', 2, 6, 'Moderado', 'Todo el año', 'Diseñado para fotógrafos de vida silvestre: 8 días en los mejores puntos fotográficos de la Amazonía peruana con guías especializados.', 'Este tour de 8 días está diseñado específicamente para fotógrafos de naturaleza. Visitamos los mejores spots de fotografía de vida silvestre en el Manu: la colpa de guacamayos de Blanquillo, latrinas de mamíferos, lagos de cochas y mucho más.', 'assets/img/hero.png', 'Wildlife Photography Tour – Manu National Park', '[]', '[{"dia":1,"titulo":"Cusco → Cloud Forest","descripcion":"Departure and first stop for cloud forest bird photography at dawn."},{"dia":2,"titulo":"Cloud Forest Photography","descripcion":"Full day shooting cloud forest wildlife: cock-of-the-rock, hummingbirds, orchids."},{"dia":3,"titulo":"Descent to Lowland Rainforest","descripcion":"Journey to the lowlands. River photography afternoon."},{"dia":4,"titulo":"Blanquillo Macaw Lick","descripcion":"Dawn at the famous macaw clay lick. Hundreds of macaws."},{"dia":5,"titulo":"Cocha Wildlife Photography","descripcion":"Kayak to a remote oxbow lake to photograph giant otters and wading birds."},{"dia":6,"titulo":"Night Photography & Mammals","descripcion":"Specialist night photography session for nocturnal mammals and insects."},{"dia":7,"titulo":"River Banks & Caiman Photography","descripcion":"Early morning boat safari for caiman photography. Afternoon river birds."},{"dia":8,"titulo":"Return to Cusco","descripcion":"Final morning shoot, return to Cusco."}]', '["Van privada","Bote"]', '2026-08-23T19:57:54.036Z');
INSERT OR REPLACE INTO tours (id, slug, nombre, categoria, estado, duracion_dias, duracion_noches, precio_desde, moneda, capacidad_min, capacidad_max, dificultad, temporada, descripcion_corta, descripcion_larga, imagen_hero, imagen_alt, galeria_json, itinerario_json, transporte_json, created_at) VALUES ('rainforest-road-trip', 'rainforest-road-trip-from-cusco', 'Rainforest Road Trip Overview', 'roadtrip', 'activo', 4, 3, 380, 'USD', 1, 3, 'Fácil', 'Abril a Noviembre (no disponible diciembre-marzo)', 'El tour más auténtico de la Amazonía peruana: un viaje en 4x4 por las aldeas y paisajes del camino de Cusco a Manu. Presupuesto amigable.', 'El Rainforest Road Trip es nuestra opción más económica y auténtica. Viajamos en 4x4 privado por el sinuoso camino de Cusco a Manu, parando en aldeas locales, probando comida tradicional y viendo fauna en el bosque nuboso.', 'assets/img/hero.png', 'Rainforest Road Trip from Cusco to Manu', '[]', '[{"dia":1,"titulo":"Cusco → Cloud Forest Villages","descripcion":"4x4 departure, visit local villages in the cloud forest."},{"dia":2,"titulo":"Deeper into the Jungle","descripcion":"Continue towards the rainforest. Swimming in natural pools. Wildlife spotting."},{"dia":3,"titulo":"Jungle Exploration","descripcion":"Walks in the lowland forest. Local food experience."},{"dia":4,"titulo":"Return to Cusco","descripcion":"Return drive with stops along the way."}]', '["4x4 privado"]', '2026-08-23T19:57:54.036Z');
INSERT OR REPLACE INTO tours (id, slug, nombre, categoria, estado, duracion_dias, duracion_noches, precio_desde, moneda, capacidad_min, capacidad_max, dificultad, temporada, descripcion_corta, descripcion_larga, imagen_hero, imagen_alt, galeria_json, itinerario_json, transporte_json, created_at) VALUES ('2-day-rainforest-road-trip', '2-day-rainforest-road-trip', '2-Day Road Trip', 'roadtrip', 'activo', 2, 1, 260, 'USD', 1, 4, 'Fácil', 'Abril a Noviembre', 'Un viaje corto en 4x4 por la ruta de los Andes hacia el bosque nuboso y la entrada a la selva del Manu.', 'Escápate 2 días a la selva en una emocionante travesía 4x4 desde Cusco. Ideal para quienes disponen de poco tiempo pero quieren cruzar los Andes y sentir la magia de la Amazonía.', 'assets/img/hero.png', '2-Day Rainforest Road Trip – Manu National Park', '[]', '[{"dia":1,"titulo":"Cusco → Cloud Forest Villages","descripcion":"Salida en 4x4 desde Cusco atravesando los Andes hacia el bosque nuboso. Observación de aves y estadía en lodge local."},{"dia":2,"titulo":"Jungle Exploration → Retorno a Cusco","descripcion":"Caminata matutina por senderos naturales y viaje de retorno a Cusco por la tarde."}]', '["4x4 privado"]', '2026-08-23T19:57:54.036Z');
INSERT OR REPLACE INTO tours (id, slug, nombre, categoria, estado, duracion_dias, duracion_noches, precio_desde, moneda, capacidad_min, capacidad_max, dificultad, temporada, descripcion_corta, descripcion_larga, imagen_hero, imagen_alt, galeria_json, itinerario_json, transporte_json, created_at) VALUES ('5-day-rainforest-road-trip', '5-day-rainforest-road-trip', '5-Day Road Trip', 'roadtrip', 'activo', 5, 4, 480, 'USD', 1, 4, 'Fácil', 'Abril a Noviembre', 'Travesía completa de 5 días en 4x4 recorriendo los valles andinos, el bosque nuboso y los ríos de la selva baja del Manu.', 'Una aventura épica por tierra y río recorriendo las comunidades y reservas naturales entre Cusco y el Manu.', 'assets/img/hero.png', '5-Day Rainforest Road Trip – Manu National Park', '[]', '[{"dia":1,"titulo":"Cusco → Paucartambo → Bosque Nuboso","descripcion":"Ruta panorámica andina con paradas fotográficas y avistamiento del Gallito de las Rocas."},{"dia":2,"titulo":"Descenso a la Selva Baja","descripcion":"Exploración de cascadas naturales, comunidades locales y navegación inicial."},{"dia":3,"titulo":"Inmersión en Selva Primaria","descripcion":"Caminatas diurnas y nocturnas para avistar monos, caimanes y vida silvestre."},{"dia":4,"titulo":"Río y Cultura Local","descripcion":"Safari fluvial, pesca tradicional y vivencia comunitaria."},{"dia":5,"titulo":"Retorno a Cusco","descripcion":"Desayuno y retorno en 4x4 hacia la ciudad de Cusco."}]', '["4x4 privado"]', '2026-08-23T19:57:54.036Z');
INSERT OR REPLACE INTO tours (id, slug, nombre, categoria, estado, duracion_dias, duracion_noches, precio_desde, moneda, capacidad_min, capacidad_max, dificultad, temporada, descripcion_corta, descripcion_larga, imagen_hero, imagen_alt, galeria_json, itinerario_json, transporte_json, created_at) VALUES ('5-day-amazon-expedition', '5-day-amazon-expedition', '5-Day Amazon Expedition', 'expedition', 'activo', 5, 4, 1200, 'USD', 2, 8, 'Moderado', 'Mayo a Octubre', 'Para aventureros serios: 5 días de expedición profunda en la selva, acampando, pescando, aprendiendo supervivencia y alejándose de la civilización.', 'La Expedición Amazónica de 5 días es para quienes quieren realmente sumergirse en la selva. Dormimos en campamentos, pescamos piranhas, aprendemos técnicas de supervivencia y exploramos áreas remotas que los tours convencionales no alcanzan.', '/media/1786591103305-pteronura-brasiliensis-zoo-brasilia-01.jpg', '5-Day Amazon Expedition from Cusco', '[]', '[{"dia":1,"titulo":"Cusco → Jungle Base Camp","descripcion":"Travel to the jungle and set up base camp."},{"dia":2,"titulo":"River Expedition","descripcion":"Full day boat expedition deep into the Amazon. Fishing and wildlife."},{"dia":3,"titulo":"Survival Skills","descripcion":"Learn to build shelters, find food, navigate without technology."},{"dia":4,"titulo":"Deep Forest Trek","descripcion":"Long day hike in rubber boots into primary rainforest. Night camping."},{"dia":5,"titulo":"Return to Cusco","descripcion":"Pack up camp and return to Cusco."}]', '["Van privada","Bote","Senderismo"]', '2026-08-23T19:57:54.036Z');
INSERT OR REPLACE INTO tours (id, slug, nombre, categoria, estado, duracion_dias, duracion_noches, precio_desde, moneda, capacidad_min, capacidad_max, dificultad, temporada, descripcion_corta, descripcion_larga, imagen_hero, imagen_alt, galeria_json, itinerario_json, transporte_json, created_at) VALUES ('6-day-amazon-expedition', '6-day-amazon-expedition', '6-Day Amazon Expedition', 'expedition', 'activo', 6, 5, 860, 'USD', 2, 8, 'Difícil', 'Mayo a Octubre', 'La expedición más completa: 6 días de aventura profunda en la selva amazónica para viajeros en busca de una experiencia realmente salvaje.', 'La Expedición Amazónica de 6 días agrega un día completo de exploración comparado con la versión de 5 días, permitiendo llegar a áreas aún más remotas del Parque Nacional Manu.', 'assets/img/hero.png', '6-Day Amazon Expedition from Cusco', '[]', '[{"dia":1,"titulo":"Cusco → Base Camp","descripcion":"Travel and setup."},{"dia":2,"titulo":"River Expedition","descripcion":"Deep river exploration."},{"dia":3,"titulo":"Survival Day 1","descripcion":"Survival skills training in the jungle."},{"dia":4,"titulo":"Remote Forest Trek","descripcion":"Long trek into remote primary forest."},{"dia":5,"titulo":"Deep Amazon Camp","descripcion":"Final night deep in the jungle."},{"dia":6,"titulo":"Return to Cusco","descripcion":"Return journey."}]', '["Van privada","Bote","Senderismo"]', '2026-08-23T19:57:54.036Z');
INSERT OR REPLACE INTO tours (id, slug, nombre, categoria, estado, duracion_dias, duracion_noches, precio_desde, moneda, capacidad_min, capacidad_max, dificultad, temporada, descripcion_corta, descripcion_larga, imagen_hero, imagen_alt, galeria_json, itinerario_json, transporte_json, created_at) VALUES ('7-day-deep-amazon-wildlife-quest', '7-day-deep-amazon-wildlife-quest', '7-Day Deep Amazon Wildlife Quest', 'wildlife', 'activo', 7, 6, 1300, 'USD', 2, 8, 'Fácil', 'Mayo - Noviembre (Temporada Seca)', 'An in-depth 7-day wildlife expedition deep into the pristine primary rainforest of Manu National Park, searching for jaguars, tapirs, giant river otters, and macaws.', 'Our 7-Day Deep Amazon Wildlife Quest takes you deep into the heart of the Manu Biosphere Reserve. Journey through the mystical cloud forest of the Andes down to the Amazonian lowlands. Navigate winding rivers, explore hidden oxbow lakes (cochas) on silent catamarans, visit world-renowned macaw clay licks (colpas), and spend nights listening to the symphony of the jungle at our comfortable rainforest lodges with professional bilingual naturalist guides.', '/media/1786591103305-pteronura-brasiliensis-zoo-brasilia-01.jpg', '7-Day Deep Amazon Wildlife Quest in Manu National Park', '[{"url":"assets/media_to_upload/photos/placeholder.jpg","alt":"Amazon Wildlife Expedition"}]', '[{"dia":1,"titulo":"Cusco → Andes Mountain Pass → Cloud Forest Lodge","descripcion":"Early morning pick-up from your hotel in Cusco (5:30 AM). Scenic drive over the Andes with stops at pre-Inca Ninamarca chullpas and the folkloric town of Paucartambo. Descend into the lush Cloud Forest of Manu to spot the Andean Cock-of-the-Rock (Peru''s national bird), woolly monkeys, and orchids. Night walk near the lodge."},{"dia":2,"titulo":"Cloud Forest → Atalaya Port → Rainforest Lodge","descripcion":"Morning birdwatching walk. Continue driving to Atalaya river port, transition to motorized dugout canoe, and navigate down the Madre de Dios River. Spotting herons, kingfishers, and sunbathing caimans. Afternoon trek along primary forest trails with introduction to medicinal plants."},{"dia":3,"titulo":"Machu Wasi Oxbow Lake & Mammal Clay Lick","descripcion":"Dawn excursion to Machu Wasi Lake on traditional balsa rafts to observe prehistoric hoatzin birds, horned screamers, capybaras, and monkeys. In the evening, visit a natural tapir clay lick platform for a night vigil."},{"dia":4,"titulo":"Deep River Navigation → Blanquillo Biological Station","descripcion":"Embark on an extended boat expedition further downriver into deeper rainforest sectors. High probability of encountering river wildlife such as side-necked turtles, capybara families, and elusive jaguars on the beaches. Settle into Blanquillo Lodge."},{"dia":5,"titulo":"Blanquillo Macaw Clay Lick & Cocha Blanco Lake","descripcion":"Early 5:00 AM departure to the hidden macaw clay lick blind. Witness hundreds of red-and-green macaws, parrots, and parakeets gathering in a spectacle of color. Afternoon exploration of Cocha Blanco to search for the resident family of Giant River Otters (*Pteronura brasiliensis*)."},{"dia":6,"titulo":"Canopy Tower Observation & Primary Rainforest Treks","descripcion":"Climb the 42-meter canopy observation tower for breathtaking panoramic views across the Amazon treetops, perfect for toucans, cotingas, and raptors. Afternoon deep forest exploration focusing on ancient giant ceiba trees and diverse monkey troops."},{"dia":7,"titulo":"Upriver Return Boat Trip → Cusco","descripcion":"Early morning upriver boat ride back to Atalaya port. Transfer to our private van for the scenic return journey through the Andes, arriving in Cusco around 7:00 PM."}]', '["Van privada","Bote a motor"]', '2026-08-23T19:57:54.036Z');
INSERT OR REPLACE INTO departures (id, tour_id, tour_nombre, fecha_salida, fecha_retorno, cupos_totales, precio, moneda, guia_asignado, estado, created_at) VALUES ('DEP-0014', '5-day-wildlife-quest-nuevo-eden', '5-Day Wildlife Quest – Nuevo Eden', '2026-08-28', '', 8, 1850, 'USD', 'Jordy Lonidas Llaqui Chusi', 'disponible', '2026-08-23T19:57:54.037Z');
INSERT OR REPLACE INTO passengers (id, departure_id, nombre_completo, nacionalidad, fecha_nacimiento, pasaporte, whatsapp, email, restricciones_dieteticas, condiciones_medicas, costo, monto_pagado, saldo_pendiente, estado_pago, foto, created_at) VALUES ('pax_DEP-0014_1', 'DEP-0014', 'Marcelo Viera', 'Francesa (FRA)', '1985-01-15', '46989140', '51958113016', 'manujungleforever@gmail.com', 'Intolerante a la Lactosa', 'Alergia a Picaduras (Abejas)', 1200, 700, 500, 'reserva', '/media/usuarios/kemmesik-gmail-com/avatar_1787257830305.jpg', '2026-08-23T19:57:54.037Z');
INSERT OR REPLACE INTO departures (id, tour_id, tour_nombre, fecha_salida, fecha_retorno, cupos_totales, precio, moneda, guia_asignado, estado, created_at) VALUES ('DEP-0013', '5-day-amazon-expedition', '5-Day Amazon Expedition', '2026-08-26', '', 8, 1250, 'USD', 'Jordy Lonidas Llaqui Chusi', 'disponible', '2026-08-23T19:57:54.037Z');
INSERT OR REPLACE INTO departures (id, tour_id, tour_nombre, fecha_salida, fecha_retorno, cupos_totales, precio, moneda, guia_asignado, estado, created_at) VALUES ('DEP-012', '7-day-deep-amazon-wildlife-quest', '7-Day Deep Amazon Wildlife Quest', '2026-08-31', '', 8, 1100, 'USD', 'Jordy Lonidas Llaqui Chusi', 'disponible', '2026-08-23T19:57:54.037Z');
INSERT OR REPLACE INTO passengers (id, departure_id, nombre_completo, nacionalidad, fecha_nacimiento, pasaporte, whatsapp, email, restricciones_dieteticas, condiciones_medicas, costo, monto_pagado, saldo_pendiente, estado_pago, foto, created_at) VALUES ('pax_DEP-012_1', 'DEP-012', 'Pablo Neruda', 'Chilena (CHI)', '1989-12-13', '46989140', '+51958113016', 'manujungleforever@gmail.com', 'Vegano', 'Problemas Cardíacos', 1200, 600, 600, 'reserva', '/media/pasajeros/dep-012_7-day-deep-amazon-wildlife-quest_2026-08-31/pablo-neruda.jpg', '2026-08-23T19:57:54.037Z');
INSERT OR REPLACE INTO departures (id, tour_id, tour_nombre, fecha_salida, fecha_retorno, cupos_totales, precio, moneda, guia_asignado, estado, created_at) VALUES ('dep-011', '6-day-wildlife-quest-blanquillo', '6-Day Wildlife Quest – Blanquillo(rapido)', '2026-08-26', '', 8, 500, 'USD', 'Jordy Lonidas Llaqui Chusi', 'completo', '2026-08-23T19:57:54.037Z');
INSERT OR REPLACE INTO departures (id, tour_id, tour_nombre, fecha_salida, fecha_retorno, cupos_totales, precio, moneda, guia_asignado, estado, created_at) VALUES ('dep-010', '6-day-wildlife-quest-reserved-zone', 'Manu Reserved Zone – 6 Days', '2026-09-10', '', 8, 1400, 'USD', '', 'disponible', '2026-08-23T19:57:54.037Z');
INSERT OR REPLACE INTO passengers (id, departure_id, nombre_completo, nacionalidad, fecha_nacimiento, pasaporte, whatsapp, email, restricciones_dieteticas, condiciones_medicas, costo, monto_pagado, saldo_pendiente, estado_pago, foto, created_at) VALUES ('pax_dep-010_1', 'dep-010', 'Pasajero de Prueba 2', '_custom_', '', 'P100001', '+1234567890', 'test1@example.com', 'Ninguna', 'Ninguna', 1400, 200, 1000, 'reserva', '/media/1787048487504-pasajeros-dep-010-manu-reserved-zone---6-days-2026-09-10-pasajero-de-prueba-2-1787048484532.jpg', '2026-08-23T19:57:54.037Z');
INSERT OR REPLACE INTO passengers (id, departure_id, nombre_completo, nacionalidad, fecha_nacimiento, pasaporte, whatsapp, email, restricciones_dieteticas, condiciones_medicas, costo, monto_pagado, saldo_pendiente, estado_pago, foto, created_at) VALUES ('pax-dep-010-2', 'dep-010', 'Pasajero de Prueba 3', 'US', '', 'P100002', '+1234567890', 'test2@example.com', '', '', 1200, 1200, 0, 'pagado', '', '2026-08-23T19:57:54.037Z');
INSERT OR REPLACE INTO passengers (id, departure_id, nombre_completo, nacionalidad, fecha_nacimiento, pasaporte, whatsapp, email, restricciones_dieteticas, condiciones_medicas, costo, monto_pagado, saldo_pendiente, estado_pago, foto, created_at) VALUES ('pax_dep-010_3', 'dep-010', 'Idel Everardo Maza Maza', 'Peruana (PER)', '1989-12-13', '46989140', '958113016', 'kemmesik@gmail.com', 'Ninguna', 'Ninguna', 1200, 100, 1100, 'reserva', '/media/1786948316933-313417303-5480125758731945-1337653701012931777-n.jpg', '2026-08-23T19:57:54.037Z');
INSERT OR REPLACE INTO passengers (id, departure_id, nombre_completo, nacionalidad, fecha_nacimiento, pasaporte, whatsapp, email, restricciones_dieteticas, condiciones_medicas, costo, monto_pagado, saldo_pendiente, estado_pago, foto, created_at) VALUES ('pax_dep-010_4', 'dep-010', 'Johan Miro', 'Estadounidense (USA)', '1987-12-13', '46989140', '+51 958 113 016', 'kemmesik@gmail.com', 'Vegetariano', 'Asma', 1400, 200, 1200, 'reserva', '/media/1787074120429-fb-img-1645218643713.jpg', '2026-08-23T19:57:54.037Z');
INSERT OR REPLACE INTO passengers (id, departure_id, nombre_completo, nacionalidad, fecha_nacimiento, pasaporte, whatsapp, email, restricciones_dieteticas, condiciones_medicas, costo, monto_pagado, saldo_pendiente, estado_pago, foto, created_at) VALUES ('pax_dep-010_5', 'dep-010', 'Maicelo Rojas', 'Peruana (PER)', '1988-05-12', '46989140', '+51958113016', 'manujungleforever@gmail.com', 'Vegetariano', 'Diabetes', 1400, 200, 1200, 'reserva', '/media/1787077673119-fb-img-1644970040656.jpg', '2026-08-23T19:57:54.037Z');
INSERT OR REPLACE INTO passengers (id, departure_id, nombre_completo, nacionalidad, fecha_nacimiento, pasaporte, whatsapp, email, restricciones_dieteticas, condiciones_medicas, costo, monto_pagado, saldo_pendiente, estado_pago, foto, created_at) VALUES ('pax_dep-010_6', 'dep-010', 'Joan Pascual', 'Estadounidense (USA)', '1989-12-13', '46989140', '+51958113016', 'manujungleforever@gmail.com', 'Vegetariano', 'Ninguna', 1400, 600, 800, 'reserva', '/media/pasajeros/dep-010_manu-reserved-zone-6-days_2026-09-10/joan-pascual.png', '2026-08-23T19:57:54.037Z');
INSERT OR REPLACE INTO departures (id, tour_id, tour_nombre, fecha_salida, fecha_retorno, cupos_totales, precio, moneda, guia_asignado, estado, created_at) VALUES ('dep-009', '6-day-wildlife-quest-blanquillo', '6-Day Wildlife Quest – Blanquillo', '2026-09-01', '', 8, 890, 'USD', '', 'disponible', '2026-08-23T19:57:54.037Z');
INSERT OR REPLACE INTO departures (id, tour_id, tour_nombre, fecha_salida, fecha_retorno, cupos_totales, precio, moneda, guia_asignado, estado, created_at) VALUES ('dep-008', '5-day-wildlife-quest-nuevo-eden', '5-Day Wildlife Quest – Nuevo Eden', '2026-08-20', '', 8, 680, 'USD', '', 'cerrado', '2026-08-23T19:57:54.037Z');
INSERT OR REPLACE INTO passengers (id, departure_id, nombre_completo, nacionalidad, fecha_nacimiento, pasaporte, whatsapp, email, restricciones_dieteticas, condiciones_medicas, costo, monto_pagado, saldo_pendiente, estado_pago, foto, created_at) VALUES ('pax-dep-008-0', 'dep-008', 'Pasajero de Prueba 1', 'US', '', 'P100000', '+1234567890', 'test0@example.com', 'Vegetariano', '', 680, 680, 0, 'pagado', '', '2026-08-23T19:57:54.037Z');
INSERT OR REPLACE INTO passengers (id, departure_id, nombre_completo, nacionalidad, fecha_nacimiento, pasaporte, whatsapp, email, restricciones_dieteticas, condiciones_medicas, costo, monto_pagado, saldo_pendiente, estado_pago, foto, created_at) VALUES ('pax-dep-008-1', 'dep-008', 'Pasajero de Prueba 2', 'US', '', 'P100001', '+1234567890', 'test1@example.com', '', '', 680, 200, 480, 'reserva', '', '2026-08-23T19:57:54.037Z');
INSERT OR REPLACE INTO passengers (id, departure_id, nombre_completo, nacionalidad, fecha_nacimiento, pasaporte, whatsapp, email, restricciones_dieteticas, condiciones_medicas, costo, monto_pagado, saldo_pendiente, estado_pago, foto, created_at) VALUES ('pax-dep-008-2', 'dep-008', 'Pasajero de Prueba 3', 'US', '', 'P100002', '+1234567890', 'test2@example.com', '', '', 680, 680, 0, 'pagado', '', '2026-08-23T19:57:54.037Z');
INSERT OR REPLACE INTO passengers (id, departure_id, nombre_completo, nacionalidad, fecha_nacimiento, pasaporte, whatsapp, email, restricciones_dieteticas, condiciones_medicas, costo, monto_pagado, saldo_pendiente, estado_pago, foto, created_at) VALUES ('pax-dep-008-3', 'dep-008', 'Pasajero de Prueba 4', 'US', '', 'P100003', '+1234567890', 'test3@example.com', '', '', 680, 200, 480, 'reserva', '', '2026-08-23T19:57:54.037Z');
INSERT OR REPLACE INTO passengers (id, departure_id, nombre_completo, nacionalidad, fecha_nacimiento, pasaporte, whatsapp, email, restricciones_dieteticas, condiciones_medicas, costo, monto_pagado, saldo_pendiente, estado_pago, foto, created_at) VALUES ('pax-dep-008-4', 'dep-008', 'Pasajero de Prueba 5', 'US', '', 'P100004', '+1234567890', 'test4@example.com', '', '', 680, 680, 0, 'pagado', '', '2026-08-23T19:57:54.037Z');
INSERT OR REPLACE INTO passengers (id, departure_id, nombre_completo, nacionalidad, fecha_nacimiento, pasaporte, whatsapp, email, restricciones_dieteticas, condiciones_medicas, costo, monto_pagado, saldo_pendiente, estado_pago, foto, created_at) VALUES ('pax-dep-008-5', 'dep-008', 'Pasajero de Prueba 6', 'US', '', 'P100005', '+1234567890', 'test5@example.com', '', '', 680, 200, 480, 'reserva', '', '2026-08-23T19:57:54.037Z');
INSERT OR REPLACE INTO passengers (id, departure_id, nombre_completo, nacionalidad, fecha_nacimiento, pasaporte, whatsapp, email, restricciones_dieteticas, condiciones_medicas, costo, monto_pagado, saldo_pendiente, estado_pago, foto, created_at) VALUES ('pax-dep-008-6', 'dep-008', 'Pasajero de Prueba 7', 'US', '', 'P100006', '+1234567890', 'test6@example.com', '', '', 680, 680, 0, 'pagado', '', '2026-08-23T19:57:54.037Z');
INSERT OR REPLACE INTO passengers (id, departure_id, nombre_completo, nacionalidad, fecha_nacimiento, pasaporte, whatsapp, email, restricciones_dieteticas, condiciones_medicas, costo, monto_pagado, saldo_pendiente, estado_pago, foto, created_at) VALUES ('pax-dep-008-7', 'dep-008', 'Pasajero de Prueba 8', 'US', '', 'P100007', '+1234567890', 'test7@example.com', '', '', 680, 200, 480, 'reserva', '', '2026-08-23T19:57:54.037Z');
INSERT OR REPLACE INTO departures (id, tour_id, tour_nombre, fecha_salida, fecha_retorno, cupos_totales, precio, moneda, guia_asignado, estado, created_at) VALUES ('dep-007', '8-day-wildlife-photography-tour', 'Wildlife Photography Tour – 8 Days', '2026-08-19', '', 8, 1450, 'USD', '', 'cerrado', '2026-08-23T19:57:54.037Z');
INSERT OR REPLACE INTO passengers (id, departure_id, nombre_completo, nacionalidad, fecha_nacimiento, pasaporte, whatsapp, email, restricciones_dieteticas, condiciones_medicas, costo, monto_pagado, saldo_pendiente, estado_pago, foto, created_at) VALUES ('pax-dep-007-0', 'dep-007', 'Pasajero de Prueba 1', 'US', '', 'P100000', '+1234567890', 'test0@example.com', 'Vegetariano', '', 1450, 1450, 0, 'pagado', '', '2026-08-23T19:57:54.037Z');
INSERT OR REPLACE INTO passengers (id, departure_id, nombre_completo, nacionalidad, fecha_nacimiento, pasaporte, whatsapp, email, restricciones_dieteticas, condiciones_medicas, costo, monto_pagado, saldo_pendiente, estado_pago, foto, created_at) VALUES ('pax-dep-007-1', 'dep-007', 'Pasajero de Prueba 2', 'US', '', 'P100001', '+1234567890', 'test1@example.com', '', '', 1450, 200, 1250, 'reserva', '', '2026-08-23T19:57:54.037Z');
INSERT OR REPLACE INTO departures (id, tour_id, tour_nombre, fecha_salida, fecha_retorno, cupos_totales, precio, moneda, guia_asignado, estado, created_at) VALUES ('dep-006', '4-day-wildlife-quest-nuevo-eden', '4-Day Wildlife Quest – Nuevo Eden', '2026-08-21', '', 8, 560, 'USD', '', 'cerrado', '2026-08-23T19:57:54.037Z');
INSERT OR REPLACE INTO passengers (id, departure_id, nombre_completo, nacionalidad, fecha_nacimiento, pasaporte, whatsapp, email, restricciones_dieteticas, condiciones_medicas, costo, monto_pagado, saldo_pendiente, estado_pago, foto, created_at) VALUES ('pax-dep-006-0', 'dep-006', 'Pasajero de Prueba 1', 'US', '', 'P100000', '+1234567890', 'test0@example.com', 'Vegetariano', '', 560, 560, 0, 'pagado', '', '2026-08-23T19:57:54.037Z');
INSERT OR REPLACE INTO departures (id, tour_id, tour_nombre, fecha_salida, fecha_retorno, cupos_totales, precio, moneda, guia_asignado, estado, created_at) VALUES ('dep-005', '3-day-wildlife-quest-machu-wasi', '3-Day Wildlife Quest – Machu Wasi', '2026-09-01', '', 8, 450, 'USD', '', 'disponible', '2026-08-23T19:57:54.037Z');
INSERT OR REPLACE INTO departures (id, tour_id, tour_nombre, fecha_salida, fecha_retorno, cupos_totales, precio, moneda, guia_asignado, estado, created_at) VALUES ('dep-004', '6-day-wildlife-quest-blanquillo', '6-Day Wildlife Quest – Blanquillo', '2026-07-20', '', 8, 890, 'USD', '', 'cerrado', '2026-08-23T19:57:54.037Z');
INSERT OR REPLACE INTO passengers (id, departure_id, nombre_completo, nacionalidad, fecha_nacimiento, pasaporte, whatsapp, email, restricciones_dieteticas, condiciones_medicas, costo, monto_pagado, saldo_pendiente, estado_pago, foto, created_at) VALUES ('pax-dep-004-0', 'dep-004', 'Pasajero de Prueba 1', 'US', '', 'P100000', '+1234567890', 'test0@example.com', 'Vegetariano', '', 890, 890, 0, 'pagado', '', '2026-08-23T19:57:54.037Z');
INSERT OR REPLACE INTO passengers (id, departure_id, nombre_completo, nacionalidad, fecha_nacimiento, pasaporte, whatsapp, email, restricciones_dieteticas, condiciones_medicas, costo, monto_pagado, saldo_pendiente, estado_pago, foto, created_at) VALUES ('pax-dep-004-1', 'dep-004', 'Pasajero de Prueba 2', 'US', '', 'P100001', '+1234567890', 'test1@example.com', '', '', 890, 200, 690, 'reserva', '', '2026-08-23T19:57:54.037Z');
INSERT OR REPLACE INTO passengers (id, departure_id, nombre_completo, nacionalidad, fecha_nacimiento, pasaporte, whatsapp, email, restricciones_dieteticas, condiciones_medicas, costo, monto_pagado, saldo_pendiente, estado_pago, foto, created_at) VALUES ('pax-dep-004-2', 'dep-004', 'Pasajero de Prueba 3', 'US', '', 'P100002', '+1234567890', 'test2@example.com', '', '', 890, 890, 0, 'pagado', '', '2026-08-23T19:57:54.037Z');
INSERT OR REPLACE INTO passengers (id, departure_id, nombre_completo, nacionalidad, fecha_nacimiento, pasaporte, whatsapp, email, restricciones_dieteticas, condiciones_medicas, costo, monto_pagado, saldo_pendiente, estado_pago, foto, created_at) VALUES ('pax-dep-004-3', 'dep-004', 'Pasajero de Prueba 4', 'US', '', 'P100003', '+1234567890', 'test3@example.com', '', '', 890, 200, 690, 'reserva', '', '2026-08-23T19:57:54.037Z');
INSERT OR REPLACE INTO passengers (id, departure_id, nombre_completo, nacionalidad, fecha_nacimiento, pasaporte, whatsapp, email, restricciones_dieteticas, condiciones_medicas, costo, monto_pagado, saldo_pendiente, estado_pago, foto, created_at) VALUES ('pax-dep-004-4', 'dep-004', 'Pasajero de Prueba 5', 'US', '', 'P100004', '+1234567890', 'test4@example.com', '', '', 890, 890, 0, 'pagado', '', '2026-08-23T19:57:54.037Z');
INSERT OR REPLACE INTO passengers (id, departure_id, nombre_completo, nacionalidad, fecha_nacimiento, pasaporte, whatsapp, email, restricciones_dieteticas, condiciones_medicas, costo, monto_pagado, saldo_pendiente, estado_pago, foto, created_at) VALUES ('pax-dep-004-5', 'dep-004', 'Pasajero de Prueba 6', 'US', '', 'P100005', '+1234567890', 'test5@example.com', '', '', 890, 200, 690, 'reserva', '', '2026-08-23T19:57:54.037Z');
INSERT OR REPLACE INTO departures (id, tour_id, tour_nombre, fecha_salida, fecha_retorno, cupos_totales, precio, moneda, guia_asignado, estado, created_at) VALUES ('dep-003', '5-day-wildlife-quest-nuevo-eden', '5-Day Wildlife Quest – Nuevo Eden', '2026-07-15', '', 8, 680, 'USD', '', 'cerrado', '2026-08-23T19:57:54.037Z');
INSERT OR REPLACE INTO passengers (id, departure_id, nombre_completo, nacionalidad, fecha_nacimiento, pasaporte, whatsapp, email, restricciones_dieteticas, condiciones_medicas, costo, monto_pagado, saldo_pendiente, estado_pago, foto, created_at) VALUES ('pax-dep-003-0', 'dep-003', 'Pasajero de Prueba 1', 'US', '', 'P100000', '+1234567890', 'test0@example.com', 'Vegetariano', '', 680, 680, 0, 'pagado', '', '2026-08-23T19:57:54.037Z');
INSERT OR REPLACE INTO passengers (id, departure_id, nombre_completo, nacionalidad, fecha_nacimiento, pasaporte, whatsapp, email, restricciones_dieteticas, condiciones_medicas, costo, monto_pagado, saldo_pendiente, estado_pago, foto, created_at) VALUES ('pax-dep-003-1', 'dep-003', 'Pasajero de Prueba 2', 'US', '', 'P100001', '+1234567890', 'test1@example.com', '', '', 680, 200, 480, 'reserva', '', '2026-08-23T19:57:54.037Z');
INSERT OR REPLACE INTO departures (id, tour_id, tour_nombre, fecha_salida, fecha_retorno, cupos_totales, precio, moneda, guia_asignado, estado, created_at) VALUES ('dep-002', '4-day-wildlife-quest-machu-wasi', '4-Day Wildlife Quest – Machu Wasi', '2026-08-20', '', 8, 580, 'USD', '', 'cerrado', '2026-08-23T19:57:54.037Z');
INSERT OR REPLACE INTO passengers (id, departure_id, nombre_completo, nacionalidad, fecha_nacimiento, pasaporte, whatsapp, email, restricciones_dieteticas, condiciones_medicas, costo, monto_pagado, saldo_pendiente, estado_pago, foto, created_at) VALUES ('pax-dep-002-0', 'dep-002', 'Pasajero de Prueba 1', 'US', '', 'P100000', '+1234567890', 'test0@example.com', 'Vegetariano', '', 580, 580, 0, 'pagado', '', '2026-08-23T19:57:54.037Z');
INSERT OR REPLACE INTO passengers (id, departure_id, nombre_completo, nacionalidad, fecha_nacimiento, pasaporte, whatsapp, email, restricciones_dieteticas, condiciones_medicas, costo, monto_pagado, saldo_pendiente, estado_pago, foto, created_at) VALUES ('pax-dep-002-1', 'dep-002', 'Pasajero de Prueba 2', 'US', '', 'P100001', '+1234567890', 'test1@example.com', '', '', 580, 200, 380, 'reserva', '', '2026-08-23T19:57:54.037Z');
INSERT OR REPLACE INTO passengers (id, departure_id, nombre_completo, nacionalidad, fecha_nacimiento, pasaporte, whatsapp, email, restricciones_dieteticas, condiciones_medicas, costo, monto_pagado, saldo_pendiente, estado_pago, foto, created_at) VALUES ('pax-dep-002-2', 'dep-002', 'Pasajero de Prueba 3', 'US', '', 'P100002', '+1234567890', 'test2@example.com', '', '', 580, 580, 0, 'pagado', '', '2026-08-23T19:57:54.037Z');
INSERT OR REPLACE INTO passengers (id, departure_id, nombre_completo, nacionalidad, fecha_nacimiento, pasaporte, whatsapp, email, restricciones_dieteticas, condiciones_medicas, costo, monto_pagado, saldo_pendiente, estado_pago, foto, created_at) VALUES ('pax-dep-002-3', 'dep-002', 'Pasajero de Prueba 4', 'US', '', 'P100003', '+1234567890', 'test3@example.com', '', '', 580, 200, 380, 'reserva', '', '2026-08-23T19:57:54.037Z');
INSERT OR REPLACE INTO passengers (id, departure_id, nombre_completo, nacionalidad, fecha_nacimiento, pasaporte, whatsapp, email, restricciones_dieteticas, condiciones_medicas, costo, monto_pagado, saldo_pendiente, estado_pago, foto, created_at) VALUES ('pax-dep-002-4', 'dep-002', 'Pasajero de Prueba 5', 'US', '', 'P100004', '+1234567890', 'test4@example.com', '', '', 580, 580, 0, 'pagado', '', '2026-08-23T19:57:54.037Z');
INSERT OR REPLACE INTO departures (id, tour_id, tour_nombre, fecha_salida, fecha_retorno, cupos_totales, precio, moneda, guia_asignado, estado, created_at) VALUES ('dep-001', '3-day-wildlife-quest-machu-wasi', '3-Day Wildlife Quest – Machu Wasi', '2026-07-05', '', 8, 450, 'USD', '', 'cerrado', '2026-08-23T19:57:54.037Z');
INSERT OR REPLACE INTO passengers (id, departure_id, nombre_completo, nacionalidad, fecha_nacimiento, pasaporte, whatsapp, email, restricciones_dieteticas, condiciones_medicas, costo, monto_pagado, saldo_pendiente, estado_pago, foto, created_at) VALUES ('pax-dep-001-0', 'dep-001', 'Pasajero de Prueba 1', 'US', '', 'P100000', '+1234567890', 'test0@example.com', 'Vegetariano', '', 450, 450, 0, 'pagado', '', '2026-08-23T19:57:54.037Z');
INSERT OR REPLACE INTO passengers (id, departure_id, nombre_completo, nacionalidad, fecha_nacimiento, pasaporte, whatsapp, email, restricciones_dieteticas, condiciones_medicas, costo, monto_pagado, saldo_pendiente, estado_pago, foto, created_at) VALUES ('pax-dep-001-1', 'dep-001', 'Pasajero de Prueba 2', 'US', '', 'P100001', '+1234567890', 'test1@example.com', '', '', 450, 200, 250, 'reserva', '', '2026-08-23T19:57:54.037Z');
INSERT OR REPLACE INTO passengers (id, departure_id, nombre_completo, nacionalidad, fecha_nacimiento, pasaporte, whatsapp, email, restricciones_dieteticas, condiciones_medicas, costo, monto_pagado, saldo_pendiente, estado_pago, foto, created_at) VALUES ('pax-dep-001-2', 'dep-001', 'Pasajero de Prueba 3', 'US', '', 'P100002', '+1234567890', 'test2@example.com', '', '', 450, 450, 0, 'pagado', '', '2026-08-23T19:57:54.037Z');
INSERT OR REPLACE INTO testimonials (id, nombre, pais, tour_nombre, rating, comentario, foto, fecha, origen, estado, created_at) VALUES ('1', 'James W.', 'United Kingdom', 'Amazon Expedition', 4, 'An absolutely incredible experience. The guides were deeply knowledgeable and passionate about the rainforest. We saw giant river otters, caimans, and countless macaws. The lodge was rustic but perfectly comfortable. Highly recommend this local agency!', '/media/1786477360363-jordy.jpg', '2026-08-01', 'tripadvisor', 'publicado', '2026-08-23T19:57:54.037Z');
INSERT OR REPLACE INTO testimonials (id, nombre, pais, tour_nombre, rating, comentario, foto, fecha, origen, estado, created_at) VALUES ('2', 'Sarah T.', 'United States', 'Wildlife Quest', 5, 'The highlight of our Peru trip! Going deep into the Amazon with indigenous guides made all the difference. We felt completely safe while being totally immersed in nature. The night walks through the jungle were mind-blowing. Thank you for everything!', '/media/1787335803567-10290631_478172738980891_705162467606874687_n.jpg', '2025', 'google', 'publicado', '2026-08-23T19:57:54.037Z');
INSERT OR REPLACE INTO testimonials (id, nombre, pais, tour_nombre, rating, comentario, foto, fecha, origen, estado, created_at) VALUES ('3', 'Matteo C.', 'Italy', 'Amazon Adventure', 5, 'If you want to see untouched wilderness, this is the company to book with. No crowded tourist traps, just pure Amazon. The food was surprisingly fantastic, and seeing a jaguar resting on the riverbank is a memory I will cherish forever.', '', '2025', 'tripadvisor', 'publicado', '2026-08-23T19:57:54.037Z');
INSERT OR REPLACE INTO testimonials (id, nombre, pais, tour_nombre, rating, comentario, foto, fecha, origen, estado, created_at) VALUES ('4', 'Elena R.', 'Spain', 'Manu Reserved Zone', 5, 'Una experiencia inolvidable. Ver a los guacamayos en la colpa de arcilla y navegar por el río Manu fue mágico. El equipo de Manu Jungle Forever nos cuidó en todo momento con una calidez excepcional.', '', '2025', 'google', 'publicado', '2026-08-23T19:57:54.037Z');
INSERT OR REPLACE INTO testimonials (id, nombre, pais, tour_nombre, rating, comentario, foto, fecha, origen, estado, created_at) VALUES ('5', 'Lucas M.', 'Germany', 'Wildlife Photography', 5, 'As a wildlife photographer, this was paradise. The guides knew exactly where to spot monkeys, toucans and river otters. Flawless organization from start to finish.', '', '2025', 'web', 'publicado', '2026-08-23T19:57:54.037Z');
INSERT OR REPLACE INTO site_content (key, value, updated_at) VALUES ('home', '{
  "hero": {
    "location_tag": "Cusco, Peru · Manu National Park",
    "title": "What Will",
    "title_emphasis": "Discover?",
    "subtitle": "Visit Manu National Park from Cusco — guided jungle tours deep into the Peruvian Amazon. Local. Wild. Authentic.",
    "video_id": "mwFesIvZ5Zc",
    "video_start": 4,
    "video_end": 56,
    "cta_primary": "Book a Tour",
    "cta_tours": "See All Tours",
    "cta_about": "About Us"
  },
  "stats": [
    {
      "value": 500,
      "suffix": "+",
      "label": "Travelers Guided",
      "type": "counter"
    },
    {
      "value": 10,
      "suffix": "+",
      "label": "Years Experience",
      "type": "counter"
    },
    {
      "value": 12,
      "suffix": "",
      "label": "Tour Options",
      "type": "counter"
    },
    {
      "value": "4.9★",
      "label": "Average Rating",
      "type": "static"
    }
  ],
  "guided_tours": {
    "title": "Guided Tours",
    "subtitle": "Curated Jungle Expeditions",
    "description": "Our itineraries are meticulously designed to cater to true nature enthusiasts. From deep-forest survival treks for the intrepid explorer, to focused wildlife spotting cruises along the riverbanks, our routes guarantee a transformative encounter with the wild.",
    "categories": [
      {
        "id": "cat-1",
        "categoria": "wildlife",
        "disponible": true,
        "badge_texto": "Available Now",
        "titulo": "Jungle Wildlife Tour",
        "duracion": "3, 4, 5, 6 or 8 Days",
        "pasajeros": "2\u20138 Passengers",
        "transporte": "Van & Boat",
        "descripcion": "Manu National Park tours from Cusco where you travel by van through the cloud forest, then search for Peruvian Amazon animals by boat. See caimans, macaws, capybaras, and the elusive jaguar. Beautiful scenery, local food, incredible nature \u2014 appropriate for all travelers.",
        "boton_texto": "Explore This Tour",
        "enlace": "guided-tours/index.html#wildlife",
        "imagen": "/media/1787015599134-gayulo-animals-3524518.jpg",
        "imagen_alt": "Jungle Wildlife Tour"
      },
      {
        "id": "cat-2",
        "categoria": "roadtrip",
        "disponible": true,
        "badge_texto": "Available Now",
        "titulo": "Rainforest Road Trip",
        "duracion": "4 or 5 Days",
        "pasajeros": "1\u20133 Passengers",
        "transporte": "Private 4\u00d74",
        "descripcion": "Our most authentic Peru Amazon tour takes you through villages along the winding road from Cusco to Manu. Spot animals in the cloud forest, taste local flavors, and visit hidden gems.",
        "boton_texto": "View Details",
        "enlace": "guided-tours/index.html#rainforest",
        "imagen": "/media/1787015599134-gayulo-animals-3524518.jpg",
        "imagen_alt": "Rainforest Road Trip"
      },
      {
        "id": "cat-3",
        "categoria": "expedition",
        "disponible": true,
        "badge_texto": "Available Now",
        "titulo": "Manu Expedition",
        "duracion": "5 or 6 Days",
        "pasajeros": "2\u20138 Passengers",
        "transporte": "Van, Boat & Hiking",
        "descripcion": "Perfect for adventurous nature lovers \u2014 this expedition takes you deep into the forest. Camp, fish, hike, and learn survival skills.",
        "boton_texto": "View Details",
        "enlace": "guided-tours/index.html#amazon",
        "imagen": "/media/1787015599134-gayulo-animals-3524518.jpg",
        "imagen_alt": "Manu Expedition"
      }
    ]
  },
  "about_section": {
    "eyebrow": "Why Choose Us",
    "title": "Visit Manu National Park with a Local Company",
    "paragraphs": [
      {
        "text": "Going to the Amazon rainforest is a dream for many travelers planning their South American adventure. If you''re looking for an amazing jungle trip near Cusco, Peru, you''re in the right place."
      },
      {
        "text": "The Manu National Park is accessible by road and river from Cusco, located on the Madre de Dios and Manu rivers — tributaries to the Amazon itself. Our founder grew up in the small village of Nuevo Eden that we use as our base; the rainforest is his home."
      },
      {
        "text": "We offer multi-day guided small-group tours and can also organize independent trips to Manu. All our jungle tours can be added onto your Cusco trip while visiting Machu Picchu and the Sacred Valley. You will get a taste of local life and opportunities to see amazing creatures in their natural habitat."
      }
    ],
    "chips": [
      "Small Groups (2–8)",
      "Born-Local Guides",
      "All-Inclusive Tours",
      "Flexible Departures",
      "Guided or Independent"
    ],
    "image": "/media/1787016658101-puesta-de-sol.jpeg",
    "image_alt": "Wildlife quest at Machu Wasi – Manu National Park",
    "cta_text": "Our Full Story",
    "cta_url": "about/index.html"
  },
  "unique_section": {
    "title": "WHAT MAKES US UNIQUE?",
    "text": "Born in the heart of Manu, we are a proudly local, family-owned company. Our lodge and trail network in Nuevo Edén are not just a tourist destination, but the childhood home of our co-founder, Jordy. We firmly believe that ecotourism is the strongest and most sustainable shield to preserve the Amazon. Through our work, we aim to uplift the community and protect the species that inhabit the jungle. Without responsible tourism, this paradise would face the constant threat of deforestation and destructive agriculture. We are driven by a deep passion to share the culture, biodiversity, and spirit of Manu National Park with you.",
    "image": "/media/1787017112075-eden.jpeg",
    "image_alt": "Manu Jungle Forever Family and Guides",
    "eyebrow": "A Legacy of Conservation"
  },
  "wildlife_section": {
    "eyebrow": "Biodiversity",
    "title": "Wildlife in the Peruvian Rainforest",
    "text": "The Manu National Park is the best place to see wildlife in Peru — you will always encounter animals in their natural habitats, surrounded by a complex ecosystem. When we visit the Amazon rainforest, we explore trails looking for monkeys, macaws, insects, snakes, and more. On the river banks we search for capybaras, turtles, caimans, and even the elusive jaguar.",
    "image": "/media/1787015599134-gayulo-animals-3524518.jpg",
    "image_alt": "Manu National Park wildlife - Jaguar",
    "animals": [
      {
        "emoji": "🐆",
        "name": "Jaguar"
      },
      {
        "emoji": "🦜",
        "name": "Macaws"
      },
      {
        "emoji": "🐊",
        "name": "Caimans"
      },
      {
        "emoji": "🐒",
        "name": "Monkeys"
      },
      {
        "emoji": "🦦",
        "name": "Giant Otters"
      },
      {
        "emoji": "🐢",
        "name": "River Turtles"
      },
      {
        "emoji": "🦫",
        "name": "Capybaras"
      },
      {
        "emoji": "🐍",
        "name": "Anaconda"
      },
      {
        "emoji": "🦋",
        "name": "Butterflies"
      },
      {
        "emoji": "🐦",
        "name": "Cock-of-the-Rock"
      }
    ]
  },
  "cta_section": {
    "eyebrow": "Ready to Explore?",
    "title": "Let''s Go to the Jungle. Plan Your Trip Today.",
    "text": "Let''s Go to the Jungle. Plan Your Trip Today.",
    "image": "/media/1787018890459-letsgo.jpg",
    "btn_text": "Book a Tour",
    "btn_url": "contact/index.html"
  },
  "pillars_section": {
    "eyebrow": "Our Values",
    "title": "Our Pillars",
    "pillars": [
      {
        "icon": "fas fa-home",
        "title": "Family Business Supporting Locals",
        "text": "We live in Peru, we love Peru. We work with our family and local professionals to operate our tours to Manu National Park. Every trip you take directly supports the local community of Nuevo Eden, Peru."
      },
      {
        "icon": "fas fa-compass",
        "title": "Guided Tours or Independent Trips",
        "text": "We offer both guided tours and can also help organize independent trips for travelers who want to visit Manu with more flexibility. Whatever your style, we tailor the experience to fit you perfectly."
      },
      {
        "icon": "fas fa-leaf",
        "title": "Sustainable Tourism",
        "text": "The Amazon Rainforest is one of our planet''s most important ecosystems, and it''s in danger. We are passionate about using tourism as a positive force to care for the jungle and its inhabitants."
      }
    ]
  },
  "featured_tour_ids": [
    "wildlife-tours",
    "rainforest-road-trip",
    "amazon-expedition"
  ],
  "map_embed_url": "https://www.google.com/maps/d/embed?mid=12fWz1M5jmQ0jd8rUJY0VUfi6KnRmvnc",
  "tours_header": {
    "title": "Guided Tours",
    "subtitle": "Curated Jungle Expeditions",
    "description": "Our itineraries are meticulously designed to cater to true nature enthusiasts. From deep-forest survival treks for the intrepid explorer, to focused wildlife spotting cruises along the riverbanks, our routes guarantee a transformative encounter with the wild."
  }
}', '2026-08-23T19:57:54.037Z');
INSERT OR REPLACE INTO site_content (key, value, updated_at) VALUES ('about', '{
  "hero_image": "/media/1786897485978-133629791959893989.jpg",
  "hero_image_fallback": "../wp-content/uploads/2022/10/Hero-About-Us.jpg",
  "hero_image_alt": "Manu Jungle Forever – Familia y Guías",
  "titulo_pagina": "About Manu Jungle Forever",
  "subtitulo_pagina": "A family-run eco-tourism company born from the rainforest of Nuevo Eden, Peru.",
  "historia": {
    "eyebrow": "Our Story",
    "titulo": "Born in the Jungle",
    "paragrafos": [
      "Dear Curious Traveler,",
      "Our team at Manu Jungle Forever is excited to share your jungle travel with you. We are a family business, working with local professionals to create an unforgettable experience.",
      "The Llaqui family will welcome you and be your guides. Jordy has been a professional tour guide in the Amazon jungle for many years, and with Gloria’s dedication to conservation, they operate this project together. They have created these tours and jungle adventures to provide a unique experience in the Manu National Park.",
      "When Gloria joined the project, she brought her deep knowledge of the region to every itinerary. The Llaqui family were welcoming and generous with their time and hospitality. They organized fishing trips, ate fresh local food, swam in the river, and more.  Whereas her trip as a tourist was strictly nature-focused, this trip was a complete immersion into a totally different life. Yet, she was in the same little slice of jungle for both.",
      "Manu Jungle Forever celebrates the whole jungle: the magnificent nature, and the local life. As a traveler, you can choose your priority and focus. We offer 3 types of guided tours that range from very nature-based to very culture-based. Or, you can customize your own adventure using our beautiful jungle bungalow as your base.",
      "Let’s meet our team of jungle experts and family members that you’ll meet along the way."
    ],
    "imagen": "/media/1787022329175-bere69-the-1865639.jpg",
    "imagen_alt": "Jordy Leonidas – Founder of Manu Jungle Forever"
  },
  "mision": {
    "eyebrow": "Our Mission",
    "titulo": "Tourism as Conservation",
    "texto": "We believe that responsible, community-based ecotourism is the most powerful tool available to protect the Amazon rainforest. By making the jungle economically valuable to local communities through tourism, we create a sustainable alternative to logging and destructive agriculture. Our mission is to show visitors the extraordinary beauty of the Manu National Park while ensuring that every visit leaves a positive impact on the environment and local people.",
    "valores": [
      {
        "icono": "fas fa-home",
        "titulo": "Community First",
        "texto": "100% of our staff are local community members. Your tour dollars go directly into the village economy."
      },
      {
        "icono": "fas fa-leaf",
        "titulo": "Environmental Stewardship",
        "texto": "We practice strict Leave No Trace principles and actively participate in reforestation and wildlife monitoring programs."
      },
      {
        "icono": "fas fa-users",
        "titulo": "Small Groups Only",
        "texto": "We limit group sizes to a maximum of 8 travelers to minimize our environmental footprint and maximize personal attention."
      },
      {
        "icono": "fas fa-shield-alt",
        "titulo": "Safety & Professionalism",
        "texto": "All guides are certified in wilderness first aid. We maintain the highest safety standards without compromising adventure."
      }
    ]
  },
  "equipo": [
    {
      "nombre": "Moises Araña",
      "cargo": "Co-Founder & Head Guide",
      "bio": "Born and raised in Nuevo Eden, Moises has been guiding in the Manu National Park for over 15 years. His encyclopedic knowledge of Amazonian wildlife and his warm, engaging personality make every tour unforgettable.",
      "foto": "assets/media_to_upload/photos/placeholder.jpg",
      "especialidad": "Wildlife identification, river navigation, jungle survival"
    },
    {
      "nombre": "Rosa Araña",
      "cargo": "Co-Founder & Operations Manager",
      "bio": "Rosa manages the day-to-day operations of Manu Jungle Forever and oversees the kitchen team, ensuring that every meal served reflects the authentic flavors of the Peruvian Amazon.",
      "foto": "assets/media_to_upload/photos/placeholder.jpg",
      "especialidad": "Operations, logistics, Amazonian cuisine"
    },
    {
      "nombre": "Carlos Araña",
      "cargo": "Senior Wildlife Guide",
      "bio": "Carlos is Moises''s brother and has a particular passion for herpetology — snakes, frogs, and lizards of the Amazon. He is also an expert birder with knowledge of over 800 species of Manu birds.",
      "foto": "assets/media_to_upload/photos/placeholder.jpg",
      "especialidad": "Herpetology, birding, jungle trekking"
    }
  ],
  "numeros": [
    {
      "valor": "10+",
      "etiqueta": "Years in Business"
    },
    {
      "valor": "500+",
      "etiqueta": "Travelers Guided"
    },
    {
      "valor": "12",
      "etiqueta": "Local Staff Members"
    },
    {
      "valor": "4.9★",
      "etiqueta": "Average Rating"
    }
  ]
}', '2026-08-23T19:57:54.037Z');
INSERT OR REPLACE INTO site_content (key, value, updated_at) VALUES ('contact', '{
  "titulo_pagina": "Contact Manu Jungle Forever",
  "subtitulo_pagina": "Ready to plan your jungle adventure? Get in touch with our team.",
  "hero_image": "assets/media_to_upload/photos/placeholder.jpg",
  "contacto_principal": {
    "email": "discover@manujungleforever.com",
    "telefono_1": "+51 931 022 183",
    "telefono_2": "+51 901 525 679",
    "whatsapp": "51901525679",
    "whatsapp_texto": "Hello! I would like to learn more about your jungle trips"
  },
  "direccion": {
    "nombre": "Manu Jungle Forever",
    "calle": "17800",
    "localidad": "Nuevo Eden",
    "pais": "Peru",
    "maps_url": "https://www.google.com/maps/d/viewer?mid=12fWz1M5jmQ0jd8rUJY0VUfi6KnRmvnc",
    "maps_embed": "https://www.google.com/maps/d/embed?mid=12fWz1M5jmQ0jd8rUJY0VUfi6KnRmvnc"
  },
  "horario": {
    "dias": "Monday – Sunday",
    "horas": "8:00 AM – 8:00 PM (Peru Time)",
    "nota": "We typically respond within 24 hours"
  },
  "formulario": {
    "titulo": "Send Us a Message",
    "subtitulo": "Fill in the form below and we''ll get back to you within 24 hours.",
    "endpoint": "handlers/send-booking.php"
  },
  "cta_whatsapp": {
    "titulo": "Prefer WhatsApp?",
    "texto": "Chat with us directly on WhatsApp for instant answers about tours, availability and pricing.",
    "boton": "WhatsApp Us Now"
  }
}', '2026-08-23T19:57:54.038Z');
INSERT OR REPLACE INTO site_content (key, value, updated_at) VALUES ('global', '{
  "site_name": "Manu Jungle Forever",
  "slogan": "Local. Wild. Authentic.",
  "tagline": "Guided jungle tours from Cusco to the Manu National Park & the Peruvian Amazon.",
  "url": "https://www.manujungleforever.com",
  "email": "discover@manujungleforever.com",
  "phone_primary": "+51 931 022 183",
  "phone_secondary": "+51 901 525 679",
  "whatsapp_number": "51958113016",
  "whatsapp_text": "Hello! I would like to learn more about your jungle trips",
  "address": "Fizcarrald 17800, Nuevo Eden, Peru",
  "address_maps_url": "https://www.google.com/maps/d/viewer?mid=12fWz1M5jmQ0jd8rUJY0VUfi6KnRmvnc",
  "logo_main": "assets/media_to_upload/photos/placeholder.jpg",
  "logo_seal": "assets/media_to_upload/photos/placeholder.jpg",
  "logo_footer": "assets/media_to_upload/photos/placeholder.jpg",
  "favicon": "assets/media_to_upload/photos/placeholder.jpg",
  "apple_touch_icon": "assets/media_to_upload/photos/placeholder.jpg",
  "social": {
    "facebook": "https://www.facebook.com/manujungleforever",
    "instagram": "https://www.instagram.com/manujungleforever/",
    "tripadvisor": "#",
    "airbnb": "#",
    "whatsapp": "https://wa.me/51958113016",
    "tiktok": "#",
    "youtube": "https://www.youtube.com/@manujungleforever"
  },
  "analytics": {
    "gtm_id": "GTM-5476BC9",
    "ga_id": "GT-NS9ZNKJP"
  },
  "seo": {
    "default_title_suffix": "| Manu Jungle Forever",
    "default_description": "Explore Cusco Jungle & Manu National Park tours with Manu Jungle Forever. Immerse yourself in wildlife — book your Peruvian Amazon adventure now!",
    "default_og_image": "assets/media_to_upload/photos/placeholder.jpg"
  },
  "copyright": "Copyright © 2026 Manu Jungle Forever. All rights reserved.",
  "copyright_design": "Site design: Meyer Consulting and Management",
  "redes_sociales": {
    "facebook": "https://www.facebook.com/manujungleforever",
    "instagram": "https://www.instagram.com/manujungleforever/",
    "tripadvisor": "#",
    "airbnb": "#",
    "whatsapp": "https://wa.me/51958113016",
    "tiktok": "#"
  }
}', '2026-08-23T19:57:54.038Z');
