#!/usr/bin/env python3
import os
import yaml

LOCALES_CONFIG = {
    "es-ar": {
        "title": "La Ciencia de la Barrera Cutánea: Qué es, Cómo se Daña y Cómo Repararla",
        "description": "Descubrí qué es exactamente la barrera cutánea y el microbioma de la piel. Aprendé a identificar los síntomas de daño y los mejores métodos para restaurarla.",
        "slug": "ciencia-barrera-cutanea-microbioma",
        "local_phenomenon": "Viento Zonda",
        "region_label": "Salta, Argentina",
        "category_label": "Ciencia & Piel",
        "epigraph": {"text": "La piel no necesita más productos; necesita que la dejes defenderse.", "author": "Dra. PepaGold"},
        "summary": [
            "La barrera cutánea es una matriz de ceramidas, colesterol y ácidos grasos que retiene agua y bloquea bacterias.",
            "El manto ácido (pH 4.5-5.5) y el microbioma son tu primera línea de defensa inmunológica contra patógenos.",
            "El clima seco (como el Viento Zonda), sulfatos y exfoliación excesiva evaporan el agua y generan microfisuras.",
            "La reparación requiere higiene atraumática sin fricción, ceramidas biomiméticas (ratio 3:1:1) y prebióticos."
        ],
        "faq": [
            {"q": "¿Cuánto tarda en repararse una barrera cutánea dañada?", "a": "El ciclo de renovación celular dura entre 14 y 28 días. Con higiene atraumática y ceramidas biomiméticas sentirás alivio en 3 a 5 días y recuperación total en 4 semanas."},
            {"q": "¿Por qué me arde la cara cuando me pongo crema hidratante?", "a": "El ardor es el síntoma #1 de microfisuras en el estrato córneo. Sin cemento lipídico ni manto ácido, la crema toma contacto directo con nervios expuestos."}
        ]
    },
    "es-mx": {
        "title": "La Ciencia de la Barrera Cutánea: Qué es, Cómo se Daña y Cómo Repararla",
        "description": "Descubre qué es exactamente la barrera cutánea y el microbioma de la piel. Aprende a identificar los síntomas de daño y los mejores métodos para restaurarla.",
        "slug": "ciencia-barrera-cutanea-microbioma",
        "local_phenomenon": "Contaminación CDMX",
        "region_label": "Ciudad de México",
        "category_label": "Ciencia & Piel",
        "epigraph": {"text": "La piel no necesita más productos; necesita que la dejes defenderse.", "author": "Dra. PepaGold"},
        "summary": [
            "La barrera cutánea es una matriz de ceramidas, colesterol y ácidos grasos que retiene agua y bloquea bacterias.",
            "El manto ácido (pH 4.5-5.5) y el microbioma son tu primera línea de defensa inmunológica contra patógenos.",
            "La contaminación de la ciudad, sulfatos y exfoliación excesiva evaporan el agua y generan microfisuras.",
            "La reparación requiere higiene atraumática sin fricción, ceramidas biomiméticas (ratio 3:1:1) y prebióticos."
        ],
        "faq": [
            {"q": "¿Cuánto tarda en repararse una barrera cutánea dañada?", "a": "El ciclo de renovación celular dura entre 14 y 28 días. Con higiene atraumática sentirás alivio en 3 a 5 días y recuperación total en 4 semanas."},
            {"q": "¿Por qué me arde la cara cuando me pongo crema hidratante?", "a": "El ardor es el síntoma principal de microfisuras en el estrato córneo. La crema entra en contacto directo con terminaciones nerviosas expuestas."}
        ]
    },
    "es-es": {
        "title": "La Ciencia de la Barrera Cutánea: Qué es, Cómo se Daña y Cómo Repararla",
        "description": "Descubre qué es exactamente la barrera cutánea y el microbioma de la piel. Aprende a identificar los síntomas de daño y los mejores métodos para restaurarla.",
        "slug": "ciencia-barrera-cutanea-microbioma",
        "local_phenomenon": "Calima y Frío Peninsular",
        "region_label": "España",
        "category_label": "Ciencia & Piel",
        "epigraph": {"text": "La piel no necesita más productos; necesita que la dejes defenderse.", "author": "Dra. PepaGold"},
        "summary": [
            "La barrera cutánea es una matriz de ceramidas, colesterol y ácidos grasos que retiene agua y bloquea bacterias.",
            "El manto ácido (pH 4.5-5.5) y el microbioma son tu primera línea de defensa inmunológica contra patógenos.",
            "La calima seca, el viento y exfoliación excesiva evaporan el agua y generan microfisuras.",
            "La reparación requiere higiene atraumática sin fricción, ceramidas biomiméticas y cuidar el bolsillo a largo plazo."
        ],
        "faq": [
            {"q": "¿Cuánto tarda en repararse una barrera cutánea dañada?", "a": "El ciclo de renovación celular dura entre 14 y 28 días. Sentirás alivio en 3 a 5 días con higiene suave y recuperación total en 4 semanas."},
            {"q": "¿Por qué me pica el rostro al usar hidratante?", "a": "La picazón es síntoma de microfisuras en el estrato córneo. Sin cemento lipídico, el producto toca los nervios expuestos."}
        ]
    },
    "en-us": {
        "title": "Skin Barrier Science: What It Is, How It Breaks, and How to Repair It",
        "description": "Discover what the skin barrier and microbiome really are. Learn to identify damage symptoms and scientific methods to restore your skin.",
        "slug": "skin-barrier-science-microbiome",
        "local_phenomenon": "Santa Ana Winds",
        "region_label": "United States",
        "category_label": "Skin Science",
        "epigraph": {"text": "Your skin doesn't need more products; it needs you to let it defend itself.", "author": "Dr. PepaGold"},
        "summary": [
            "The skin barrier is a matrix of ceramides, cholesterol, and fatty acids that locks in water and blocks pathogens.",
            "The acid mantle (pH 4.5-5.5) and microbiome serve as your first line of immunological defense.",
            "Dry winds (like Santa Ana winds), harsh sulfates, and over-exfoliation strip lipids and cause micro-cracks.",
            "Repair requires gentle non-friction cleansing, biomimetic 3:1:1 lipid replacement, and prebiotics."
        ],
        "faq": [
            {"q": "How long does it take to repair a damaged skin barrier?", "a": "The cellular turnover cycle takes 14 to 28 days. With friction-free cleansing and ceramides, relief begins in 3 to 5 days, full recovery in 4 weeks."},
            {"q": "Why does moisturizer sting my face?", "a": "Stinging is the #1 sign of micro-tears in the stratum corneum. Without lipid cement or acid mantle, cream makes direct contact with exposed nerve endings."}
        ]
    },
    "fr-fr": {
        "title": "La Science de la Barrière Cutanée: Qu'est-ce que C'est et Comment la Réparer",
        "description": "Découvrez ce qu'est la barrière cutanée et le microbiome. Apprenez à identifier les symptômes de dommages et les méthodes scientifiques pour la restaurer.",
        "slug": "science-barriere-cutanee-microbiome",
        "local_phenomenon": "Eau Dure Calcaire",
        "region_label": "France",
        "category_label": "Science de la Peau",
        "epigraph": {"text": "La peau n'a pas besoin de plus de produits; elle a besoin que vous la laissiez se défendre.", "author": "Dr. PepaGold"},
        "summary": [
            "La barrière cutanée est une matrice de céramides, cholestérol et acides gras qui retient l'eau et bloque les bactéries.",
            "Le manteau acide (pH 4.5-5.5) et le microbiome constituent la première ligne de défense immunologique.",
            "L'eau dure calcaire, les sulfates et l'exfoliation excessive assèchent la peau et créent des micro-fissures.",
            "La réparation nécessite un nettoyage doux sans friction, des céramides biomimétiques et des prébiotiques."
        ],
        "faq": [
            {"q": "Combien de temps faut-il pour réparer une barrière cutanée endommagée?", "a": "Le cycle de renouvellement cellulaire dure de 14 à 28 jours. Un soulagement apparaît en 3 à 5 jours et une récupération complète en 4 semaines."},
            {"q": "Pourquoi la crème hydratante me pique-t-elle?", "a": "Les picotements sont le premier signe de micro-fissures de la couche cornée. Sans ciment lipidique, la crème touche les terminaisons nerveuses."}
        ]
    },
    "de-de": {
        "title": "Die Wissenschaft der Hautbarriere: Funktion, Schäden und Reparatur",
        "description": "Erfahren Sie, was die Hautbarriere und das Mikrobiom genau sind. Lernen Sie Symptome von Schäden und wissenschaftliche Methoden zur Wiederherstellung kennen.",
        "slug": "wissenschaft-hautbarriere-mikrobiom",
        "local_phenomenon": "Trockene Heizungsluft",
        "region_label": "Deutschland",
        "category_label": "Hautwissenschaft",
        "epigraph": {"text": "Die Haut braucht nicht mehr Produkte; sie muss sich selbst verteidigen können.", "author": "Dr. PepaGold"},
        "summary": [
            "Die Hautbarriere ist eine Matrix aus Ceramiden, Cholesterin und Fettsäuren, die Wasser bindet und Bakterien blockiert.",
            "Der Säureschutzmantel (pH 4,5-5,5) und das Mikrobiom sind die erste immunologische Verteidigungslinie.",
            "Kälte, trockene Heizungsluft und aggressive Tenside verdunsten Wasser und erzeugen Mikrorisse.",
            "Die Reparatur erfordert sanfte reibungsfreie Reinigung, biomimetische Ceramide (3:1:1 Ratio) und Präbiotika."
        ],
        "faq": [
            {"q": "Wie lange dauert die Reparatur einer beschädigten Hautbarriere?", "a": "Der ZellErneuerungszyklus dauert 14 bis 28 Tage. Schmerzlinderung tritt in 3 bis 5 Tagen ein, vollständige Heilung in 4 Wochen."},
            {"q": "Warum brennt Feuchtigkeitscreme im Gesicht?", "a": "Brennen ist das Symptom Nr. 1 für Mikrorisse in der Hornschicht. Ohne Lipidzement berührt die Creme freiliegende Nerven."}
        ]
    },
    "it-it": {
        "title": "La Scienza della Barriera Cutanea: Cos'è e Come Ripararla",
        "description": "Scopri cos'è la barriera cutanea e il microbioma. Impara a identificare i sintomi dei danni e i metodi scientifici per ripristinarla.",
        "slug": "scienza-barriera-cutanea-microbioma",
        "local_phenomenon": "Sole e Caldo Mediterraneo",
        "region_label": "Italia",
        "category_label": "Scienza della Pelle",
        "epigraph": {"text": "La pelle non ha bisogno di più prodotti; ha bisogno che la lasci difendersi.", "author": "Dott.ssa PepaGold"},
        "summary": [
            "La barriera cutanea è una matrice di ceramidi, colesterolo e acidi grassi che trattiene l'acqua e blocca i batteri.",
            "Il mantello acido (pH 4.5-5.5) e il microbioma costituiscono la prima linea di difesa immunologica.",
            "Sole intenso, aria secca e detergenti aggressivi evaporano l'acqua e creano micro-fessure.",
            "La riparazione richiede una detersione delicata senza attrito, ceramidi biomimetiche e prebiotici."
        ],
        "faq": [
            {"q": "Quanto tempo occorre per riparare una barriera cutanea danneggiata?", "a": "Il ciclo di rinnovamento cellulare dura da 14 a 28 giorni. Noterai sollievo in 3-5 giorni e pieno recupero in 4 settimane."},
            {"q": "Perché la crema idratante mi brucia?", "a": "Il bruciore è il primo segnale di micro-lesioni nello strato corneo. Senza cemento lipidico, la crema entra in contatto con i nervi."}
        ]
    },
    "pt-br": {
        "title": "A Ciência da Barreira Cutânea: O que É e Como Reparar",
        "description": "Descubra o que é a barreira cutânea e o microbioma da pele. Aprenda a identificar sinais de danos e os melhores métodos para restaurá-la.",
        "slug": "ciencia-barreira-cutanea-microbioma",
        "local_phenomenon": "Umidade Alta e Calor",
        "region_label": "Brasil",
        "category_label": "Ciência & Pele",
        "epigraph": {"text": "A pele não precisa de mais produtos; precisa que você a deixe se defender.", "author": "Dra. PepaGold"},
        "summary": [
            "A barreira cutânea é uma matriz de ceramidas, colesterol e ácidos graxos que retém água e bloqueia bactérias.",
            "O manto ácido (pH 4.5-5.5) e o microbioma são sua primeira linha de defesa imunológica contra patógenos.",
            "Sabonetes agressivos, esfoliação excessiva e poluição evaporam a água e geram microfissuras.",
            "A reparação requer higienização suave sem atrito, ceramidas biomiméticas e prebióticos."
        ],
        "faq": [
            {"q": "Quanto tempo demora para reparar uma barreira cutânea danificada?", "a": "O ciclo de renovação celular dura de 14 a 28 dias. Você sentirá alívio em 3 a 5 dias e recuperação total em 4 semanas."},
            {"q": "Por que o hidratante arde no meu rosto?", "a": "A ardência é o sintoma principal de microfissuras no estrato córneo. Sem cimento lipídico, o creme encosta diretamente nos nervos."}
        ]
    },
    "ru-ru": {
        "title": "Наука о Кожном Барьере: Что Это Такое и Как Его Восстановить",
        "description": "Узнайте, что такое кожный барьер и микробиом. Научитесь распознавать симптомы повреждений и восстанавливать кожу научно доказанными методами.",
        "slug": "nauka-kozhnij-barier-mikrobiom",
        "local_phenomenon": "Ледяной Ветер и Мороз",
        "region_label": "Россия",
        "category_label": "Наука о Коже",
        "epigraph": {"text": "Коже не нужно больше продуктов; ей нужно дать возможность защищаться самой.", "author": "Др. ПепаГолд"},
        "summary": [
            "Кожный барьер — это матрица из церамидов, холестерина и жирных кислот, удерживающая воду и блокирующая бактерии.",
            "Кислотная мантия (pH 4.5-5.5) и микробиом — первая линия иммунной защиты.",
            "Сильный мороз, сухой ветер от отопления и агрессивные павы испаряют влагу и вызывают микротрещины.",
            "Восстановление требует бережного очищения без трения, биомиметических церамидов и пребиотиков."
        ],
        "faq": [
            {"q": "Сколько времени нужно на восстановление кожного барьера?", "a": "Цикл обновления клеток длится от 14 до 28 дней. Облегчение наступит через 3-5 дней, полное восстановление — за 4 недели."},
            {"q": "Почему крем щиплет лицо при нанесении?", "a": "Щипание — признак микротрещин в роговом слое. Без липидного цемента крем сразу контактирует с нервными окончаниями."}
        ]
    },
    "zh-hans": {
        "title": "皮肤屏障的科学：构成、受损机制与修复指南",
        "description": "深入了解什么是皮肤屏障与角质层微生态。学会识别屏障受损症状，掌握科学的屏障修复方法。",
        "slug": "skin-barrier-science-microbiome",
        "local_phenomenon": "城市空气污染 PM2.5",
        "region_label": "中国",
        "category_label": "皮肤科学",
        "epigraph": {"text": "肌肤不需要堆砌过多护肤品；它需要的是恢复自我防御力。", "author": "PepaGold博士"},
        "summary": [
            "皮肤屏障是由神经酰胺、胆固醇和游离脂肪酸组成的脂质基质，用于锁水并抵抗外界细菌。",
            "弱酸性皮脂膜（pH 4.5-5.5）与皮肤微生态是人体第一道免疫防御屏障。",
            "干燥气候、强表面活性剂与过度去角质会导致水分大量流失（TEWL）并产生微细创口。",
            "屏障修复需要无摩擦温和清洁、仿生3:1:1脂质补充与益生元微生态调节。"
        ],
        "faq": [
            {"q": "受损的皮肤屏障需要多久才能修复？", "a": "皮肤细胞更新周期通常为14至28天。通过无摩擦清洁与仿生神经酰胺，3至5天内即可缓解刺痛，4周内完成全面修复。"},
            {"q": "为什么涂抹保湿霜时脸部会有刺痛感？", "a": "刺痛是角质层产生微细裂隙的首要信号。缺乏脂质包覆时，护肤品成分会直接触及暴露的神经末梢。"}
        ]
    }
}

BASE_BODY_AR = """
## **La Ciencia de la Barrera Cutánea: Qué es y Cómo Funciona**

La ciencia de la piel ha experimentado un cambio de paradigma radical. Históricamente, se creía que la capa más externa de la piel (el estrato córneo) era solo un depósito de células muertas. Hoy sabemos que es una **interfaz biológica dinámicamente activa**, un biosensor complejo y tu principal línea de defensa inmunológica e hidratante.

El concepto de "barrera cutánea" engloba un sistema multidimensional que retiene el agua de tu piel, bloquea bacterias y te protege del sol. Cuando esta barrera se rompe, aparecen problemas como sequedad extrema, dermatitis atópica, acné y rosácea.

:::stat
**30% a 50%** de los pacientes con dermatitis atópica severa presentan una mutación en el gen de la filagrina, la proteína encargada de mantener la barrera cutánea hidratada.
:::

:::funfact ¿Sabías que?
**Pérdida Transepidérmica de Agua (TEWL)**
Tu piel pierde de forma natural hasta medio litro de agua al día a través de la evaporación imperceptible. ¡Es el sistema de termorregulación más avanzado del cuerpo humano!
:::

## **Arquitectura de la Piel: Ladrillos y Cemento**

Imaginá tu piel como una pared de ladrillos:

- **Los Ladrillos (Corneocitos):** Células ultra resistentes empaquetadas con queratina que te protegen de rasguños y fricción.
- **El Cemento (Matriz Lipídica):** El pegamento biológico que mantiene unidos los ladrillos. Compuesto por **Ceramidas (50%)**, Colesterol (25%) y Ácidos Grasos Libres (15%).

:::tip El Secreto del Ratio 3:1:1
Para que el "cemento" de tu piel sea impenetrable, las ceramidas, el colesterol y los ácidos grasos deben estar en una proporción exacta de 3:1:1. Cuando busques cremas reparadoras, elegí formulaciones biomiméticas que respeten esta proporción.
:::

### El Manto Ácido: El Guardián Invisible

Por encima de esta pared de ladrillos, tu piel tiene una película de agua y sebo llamada **manto ácido**, con un pH óptimo entre 4.5 y 5.5. Este ambiente ácido desactiva bacterias dañinas y crea el hábitat ideal para el **microbioma cutáneo** (las bacterias buenas).

Si usás jabones en barra tradicionales (que son alcalinos), destruís el manto ácido. Esto detiene la producción natural de ceramidas y acelera la irritación y la descamación.

## **El Microbioma: Tu Cuarta Dimensión Protectora**

Ya no podemos pensar en la piel solo como tejido: es un ecosistema completo. Bacterias benéficas como el _Staphylococcus epidermidis_ habitan la superficie y se alimentan de lípidos naturales. A cambio, sintetizan sus propios péptidos antimicrobianos para combatir patógenos como el _Staphylococcus aureus_ (responsables de los brotes de dermatitis).

:::info Disbiosis: Cuando las bacterias buenas mueren
La disbiosis ocurre cuando alterás tu microbioma por lavado excesivo o químicos agresivos. Sin bacterias benéficas que te protejan, los patógenos proliferan, el sistema inmune reacciona y la piel se inflama, enrojece o llena de brotes.
:::

## **Factores que Destruyen tu Barrera Cutánea**

Tu piel soporta agresiones diarias, pero tiene un límite:

1. **El Clima Extremo ({local_phenomenon}):** El aire seco y cálido extrae agua de tus células. El fenómeno de {local_phenomenon} en {region_label} desploma la humedad ambiental, acelerando la evaporación transcutánea (TEWL) y creando microfisuras.
2. **Limpiadores Agresivos (Sulfatos):** Tensoactivos pesados como SLS o SLES disuelven la matriz lipídica como si fuera grasa en un sartén.
3. **Exfoliación Excesiva:** Usar ácidos o cepillos físicos con demasiada frecuencia retira capas protectoras antes de su regeneración.

:::checklist Señales de Alarma: ¿Tu barrera está rota?
- [ ] Tu piel se ve opaca y sin luz natural.
- [ ] Sientes tirantez inmediata al salir de la ducha.
- [ ] Cualquier crema que te ponés te arde o pica.
- [ ] Notas descamación y textura áspera constante.
:::

## **Cómo Reparar la Barrera Cutánea Paso a Paso**

La regla de oro para reparar la piel es **dejar de agredirla**:

1. **Higiene Atraumática:** Evitá el agua muy caliente y los jabones espumosos. Optá por limpiadores Syndet o tecnologías de microfibra física (como Laska Mini) que limpian poros por succión capilar sin remover lípidos esenciales.
2. **Reposición Lipídica:** Utilizá cremas enriquecidas con ceramidas, ácido hialurónico y escualano.
3. **Prebióticos Tópicos:** Preferí cosméticos con inulina para nutrir las bacterias benéficas y reequilibrar la flora cutánea.

:::quiz Test de Diagnóstico Cutáneo
Q: ¿Cuál es el síntoma más claro de que tu barrera cutánea perdió su cemento lipídico?
- Sensación de ardor o picazón al aplicar una crema neutra *correct*
- Piel suave y luminosa después de lavar con jabón común
- Mayor producción de colágeno en la zona T
:::

:::info ¿Mito o Verdad?
**"Si tengo piel grasa o acné, debo lavarme más seguido para secar los granos"**

**Respuesta:** ¡Mito! El acné suele ser síntoma de una barrera alterada. Al lavarte en exceso, eliminas las ceramidas y la flora protectora. Tu piel reacciona produciendo el doble de sebo para defenderse, lo que agrava los brotes.
:::

![](/assets/imagenes/blog/ciencia-barrera-cutanea-microbioma/barrera_cutanea_2.webp)
"""

def generate_all_locales():
    for code, cfg in LOCALES_CONFIG.items():
        meta = {
            "article_id": "PG-001",
            "title": cfg["title"],
            "description": cfg["description"],
            "slug": cfg["slug"],
            "date": "2026-07-17",
            "date_created": "2026-07-17",
            "date_ai_processed": "2026-07-20",
            "locale": code,
            "category": "barrera-cutanea",
            "category_label": cfg["category_label"],
            "concept": "barrera-cutanea-y-microbioma",
            "local_phenomenon": cfg["local_phenomenon"],
            "region_label": cfg["region_label"],
            "media": ["/assets/imagenes/blog/ciencia-barrera-cutanea-microbioma/barrera_cutanea_1.webp"],
            "author": "PepaGold",
            "epigraph": cfg["epigraph"],
            "summary": cfg["summary"],
            "faq": cfg["faq"],
            "related": [],
            "image_prompts": [
                "Cover: Ultra-realistic 4K macro photography of healthy human skin texture with natural glow and fine pores, no text, warm lighting.",
                "Body: Clean scientific diagram illustrating skin barrier stratum corneum layers and lipid matrix, warm minimalist style, no text."
            ],
            "show_science_link": True
        }

        body = BASE_BODY_AR.format(
            local_phenomenon=cfg["local_phenomenon"],
            region_label=cfg["region_label"]
        )

        yaml_str = yaml.dump(meta, allow_unicode=True, sort_keys=False)
        full_md = f"---\n{yaml_str}---\n{body}"

        out_dir = f"blog/posts/{code}"
        os.makedirs(out_dir, exist_ok=True)
        file_path = os.path.join(out_dir, f"{cfg['slug']}.md")

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(full_md)
        print(f"✅ Guardado: {file_path}")

if __name__ == "__main__":
    generate_all_locales()
