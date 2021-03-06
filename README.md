
####Обучение 
 - Для простого обучения вполне достаточно иметь 2 видео исходного и целевого лиц, а дальше алгоритмы определят лица в
   видео ([FaceNet](https://github.com/davidsandberg/facenet)) и оптимально извлекать кадры с лицом, по этой причине в
   кадре необходимо присутствие только и только одного лица.
 - Для лучших результатов подмены лица, количество итераций должно быть не меньше 18'000.

_Ниже представлен один из этапов процесса [обучения](docs/train.md) 
GAN нейросети для подмены лиц при различных итерациях обучения_:

**7200**

![Обучение при 7200 итерациях](docs/images/train/10k/7200/recon.png "Обучение при 7200 итерациях")

**7500**

![Обучение при 7500 итерациях](docs/images/train/10k/7500/recon.png "Обучение при 7200 итерациях")

**21k**

![Обучение при 21k итерациях](docs/images/train/20k_30k/21000/recon.png "Обучение при 7200 итерациях")

График потерь:

![](docs/images/train/loss/loss_ga.png)
![](docs/images/train/loss/loss_gb.png)
![](docs/images/train/loss/loss_da.png)
![](docs/images/train/loss/loss_db.png)

Де




## Замена частей лица

#### Способ №1

- Заменить только часть исходного лица (рот/нос/глаза) на целевое лицо, обрабатывая замененное лицо как расширенные
  обучающие данные для исходного лица.
- Для каждого исходного изображения лица аналогичное целевое лицо извлекается с помощью knn
  (с использованием усредненной карты объектов в качестве входных данных) для замены частей лица.
- Недостатки: 
  - модель также учится генерировать артефакты, которые появляются в дополненных данных, например, острые края
  вокруг глаз/носа и странно искаженное лицо.
  - артефакты дополненных данных вызваны несовершенным смешиванием (из-за ложных ориентиров и плохого perspective warping).
  - необходимо для каждой части лица выполнять обучение.

- ![](https://www.dropbox.com/s/1l9n1ple6ymxy8b/data_augm_flowchart.jpg?raw=1)

#### Способ №2

- Во время трансформации лица производим поиск ориентиров частей лица на кадре с помощью библиотеки `face-alignment` на
  исходном лице;
- Производим `convex hull` для расширения найденных точек в жирную линию;
- Производим обрисовку контуров полученного `convex hull`
- ![](docs/images/arch/face_parts_mask_b.png)
- Для того чтобы ненужные части лица были удалены, оставив только нужные, производим объединение исходного лица с
  бинарным исходного лица;
- ![](docs/images/arch/face_parts_mask_face.png)
- Производим снова masking и дальше проискодит замена лица.
- ![](docs/images/arch/partial_swapped_face.jpg)

## Google Colab

[FaceswapGAN train](https://colab.research.google.com/github/imadfndt/faceswap-parts/blob/main/colab/faceswap-demo.ipynb)
для faceswap на Google Colab.

Пользователи могут обучать свою собственную модель в браузере.

* [faceswap_train.ipynb](https://github.com/imadfndt/faceswap-parts/blob/main/colab/faceswap_train.ipynb)
    - Блокнот для обучения FaceswapGAN модели.
    - Требуются дополнительные обучающие изображения, созданные с
      помощью [prep_binary_masks.ipynb](https://github.com/imadfndt/faceswap-parts/blob/main/prep_binary_masks.ipynb).

* [faceswap_video_conversion.ipynb](https://github.com/imadfndt/faceswap-parts/blob/main/colab/faceswap_video_conversion.ipynb)
    - Ноутбук для преобразования видео FaceswapGAN модели.
    - Выравнивание лица с использованием 5-точечных ориентиров используется в преобразовании видео.

* [prep_binary_masks.ipynb](https://github.com/imadfndt/faceswap-parts/blob/main/colab/prep_binary_masks.ipynb)
    - Ноутбук для предварительной обработки обучающих данных. Выходные двоичные маски сохраняются
      в `{dir}/binary_masks/face_src_eyes` и `{dir}/binary_masks/face_dst_eyes`.
    - Требуется пакет [face_alignment](https://github.com/1adrianb/face-alignment). Альтернативный метод для генерации бинарных масок без требования библиотек `face_alignment` и `dlib`, находятся
      в [video_face_detection_alignment.ipynb](https://github.com/imadfndt/faceswap-parts/blob/main/video_face_detection_alignment.ipynb).

* [video_face_detection_alignment.ipynb](https://github.com/imadfndt/faceswap-parts/blob/main/colab/video_face_detection_alignment.ipynb)
    - Этот ноутбук выполняет распознавание/выравнивание лиц на входном видео.
    - Обнаруженные лица сохраняются в `{dir}/faces/raw_faces` и `{dir}/faces/aligned_faces` для выровненных и без
      результатов соответственно.
    - Двоичные маски глаз также генерируются и сохраняются в `{dir}/faces/binary_masks_eyes`. Эти двоичные маски могут
      служить субоптимальной альтернативой маскам, созданным с
      помощью [prep_binary_masks.ipynb](https://github.com/imadfndt/faceswap-parts/blob/main/colab/prep_binary_masks.ipynb).

### Прочее

**Как использовать?**

Выполняйте [faceswap-demo.ipynb](https://github.com/imadfndt/faceswap-parts/blob/main/colab_demo/faceswap-demo.ipynb)
для реализации всех этапов FaceSwap в одном ноутбуке (в Google Colab).

_**Примечание:**_ Для хранения обучаемых данных рекомендуется использовать Google Drive или Google Storage. В ноутбуке
есть необходимые инструкции.
_**Примечание:**_ Для реализации проекта были выбраны не самые оптимальные параметры

```python
from converter.config import (
    ConverterConfig,
    ColorCorrectionType,
    ImageOutputType,
    TransformDirection,
    SegmentationType
)

RESOLUTION=64 # возможно: 64, 128, 256
image_shape=(RESOLUTION, RESOLUTION, 3)

# для обучения
arch_config = {
        "image_shape": image_shape,
        "use_self_attn": True,  # SAGAN
        "norm": "hybrid",  # instancenorm, batchnorm, layernorm, groupnorm, none, hybrid
        "model_capacity": "lite"  # 'standard', 'lite'
    }

# для конвертации/замены
config = ConverterConfig(
    image_shape=image_shape,  
    use_smoothed_bbox=True,
    use_kalman_filter=True,
    use_auto_downscaling=False,  # для понижения разрешения изображения
    bbox_moving_avg_coef=0.65,  # если фильтры Кальмана отключены
    min_face_area=35 * 35,  # минимально допустимая площадь лица для выбора 
    kf_noise_coef=1e-3,  # коэфициент шума для фильтра Кальмана
    color_correction=ColorCorrectionType.HISTMATCH,  # коррекция цвета для замены, чтобы убрать несоответствие цветов лиц
    detection_threshold=0.8,
    roi_coverage=0.9,  # размер заменяемой части лица
    output_type=ImageOutputType.COMBINED,  # SINGLE, COMBINED, TRIPLE - формат вывода результата
    direction=TransformDirection.AtoB,  # направление для замены между двумя файлами
    segmentation=SegmentationType.EYES_ONLY  # какие части лица заменить 
)
```

Вышеописанный ноутбук состоит из ячеек, взятых из следующих ноутбуков:

- [video_face_detection_alignment.ipynb](https://github.com/imadfndt/faceswap-parts/blob/main/colab/video_face_detection_alignment.ipynb)
  для извлечения лиц из видео.
- [prep_binary_masks.ipynb](https://github.com/imadfndt/faceswap-parts/blob/main/colab/prep_binary_masks.ipynb) для
  создания двоичных масок обучающих изображений.
- [faceswap_train.ipynb](https://github.com/imadfndt/faceswap-parts/blob/main/colab/faceswap_train.ipynb) для
  обучения моделей.
- [faceswap_video_conversion.ipynb](https://github.com/imadfndt/faceswap-parts/blob/main/colab/faceswap_video_conversion.ipynb)
  для создания видео с использованием обученных моделей.

**Примечание:** *Только для ознакомительных целей*.

### Формат обучающих данных

- Face images are supposed to be in `{dir}/face_src/` or `{dir}/face_dst/` folder for source and target respectively.
- Изображения лиц должны находиться в папке `{dir}/face_src/` или `{dir}/face_dst/` для исходного и целевого лиц
  соответственно.
- Во время обучения размер изображений будет изменен до 256x256.

