---
title: NLP Projects
description: This quarter's main focus
created: February 16
modified: February 18
---
у меня пока что есть три основных инструмента:

1. topic modeling, где я могу кластеризовать и обозвать кластеры обратной связи.

- не очень точный, но дешёвый
- в рамках CSI не вызывает вау-эффекта, так как топики примерно те же, что и в CSI, но в CSI они возможно даже лучше корзинятся
- больше подходит для unknown unknowns обратной связи, где никто не маркирует топики
- попробовал взять отдельно топики про "голос" и про "пульт" и там действительно в основном не про голос и не про пульт ))

---

2. Частота двух-трёх-словных словосочетаний

- может упростить доступ к сырым данным, считая вхождения в корзине (см. видео)
- можно сделать динамически, углубляясь внутрь топика-субтопика, можно подтягивать соседние поля

---

3. классификация по известным категориям и тональности

- более точный, чем 1, позволяет смотреть % доли, но подвержен всем тем же проблемам, что описал Саша, поэтому скорее всего не более точный, чем разбивка по топикам внутри CSI
- при этом более дорогой при использовании Гиги
- можно попробовать разбивать комментарии как минимум на предложения, а возможно и запятые
- надо попробовать действительно сделать мультилейблы
- я попробовал на 200 комментариях, всё не прогонял, но вижу, что пока ошибается и в ключевую информацию попадают мультилейблы (см. image.png)