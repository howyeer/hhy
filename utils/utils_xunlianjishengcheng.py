import os
import json
import random

import cv2


class CreateCOCODataset(object):
    def __init__(self, jsons_path, images_path):
        self._categories = {"AJ": 1, "BX": 2, "CJ": 3, "CK": 4, "CQ": 5, "CR": 6, "FS": 7, "FZ": 8,
                            "JG": 9, "PL": 10, "QF": 11, "SG": 12, "SL": 13, "TJ": 14, "TL": 15, "ZW": 16}
        self._supercategories = {"functional defect": ["PL", "BX", "FS", "CK", "QF", "TJ", "TL", "AJ", "CR", "SL"],
                                 "structural defect": ["CJ", "JG", "ZE", "CQ", "SG", "FZ"]}

        self.info = self._create_info()
        self.category = self._create_categories()
        self.images = self._create_images(jsons_path, images_path)
        self.annotations = self._create_annotations(jsons_path)

    def _create_categories(self):
        categories = []
        for ca in self._categories:
            if ca in self._supercategories["functional defect"]:
                supercategory = "functional defect"
            else:
                supercategory = "structural defect"
            categories.append({
                "supercategory": supercategory,
                "id": self._categories[ca],
                "name": ca
            })
        return categories

    def _create_info(self):
        info = {
            "description": "Shi Luo De Sewer Defect Dataset",
            "version": "4.0",
            "year": "2022",
            "contributor": "University of Electronic Science and Technology of China",
            "data_created": "2022/12/01"
        }
        return info

    def _create_images(self, jsons_path, images_path):
        images = []
        idx = 1
        for json_path in jsons_path:
            data = json.load(open(json_path, "r"))
            images.append({
                "id": idx,
                "file_name": "abnormal/" + data["imagePath"],
                "width": data["imageWidth"],
                "height": data["imageHeight"]
            })
            idx += 1
        for image_path in images_path:
            file_name = os.path.split(image_path)[1]
            img = cv2.imread(image_path)
            h, w, _ = img.shape
            images.append({
                "id": idx,
                "file_name": "normal/" + file_name,
                "width": w,
                "height": h
            })
            idx += 1
        return images

    def _create_annotations(self, jsons_path):
        anno_info = []
        id = 1
        for idx, json_path in enumerate(jsons_path):
            data = json.load(open(json_path, "r"))
            for instance in data["shapes"]:
                image_id = idx + 1
                category_id = self._categories[instance["label"][:2]]
                bbox = instance["points"]
                anno_info.append([id, image_id, category_id, bbox])
                id += 1
        annotations = []
        for an_ in anno_info:
            x1, y1 = an_[3][0]
            x2, y2 = an_[3][1]
            x1 = float(x1)
            y1 = float(y1)
            w = float(x2 - x1)
            h = float(y2 - y1)
            area = w * h
            annotations.append({
                "id": an_[0],
                "image_id": an_[1],
                "category_id": an_[2],
                "bbox": [x1, y1, w, h],
                "iscrowd": 0,
                "area": float(area)
            })
        return annotations

    def create_out(self):
        out = {"info": self.info,
               "categories": self.category,
               "images": self.images,
               "annotations": self.annotations
               }
        return out


def get_json_path(annotations_path):
    n = len(os.listdir(annotations_path))
    jsons_name = [str(i).zfill(4) + ".json" for i in range(n)]
    jsons_path = [os.path.join(annotations_path, json_name) for json_name in jsons_name]
    return jsons_path


def get_image_path(images_path):
    n = len(os.listdir(images_path))
    imgs_path = [os.path.join(images_path, img_name) for img_name in os.listdir(images_path)]
    imgs_dict = {}
    for img_path in imgs_path:
        img_idx = int(os.path.split(img_path)[1].split(".")[0])
        imgs_dict[img_idx] = img_path
    imgs_list = []
    for i in range(n):
        imgs_list.append(imgs_dict[i])
    return imgs_list


if __name__ == "__main__":
    root = "E:\\code\Dataset\\ShiLuoDeDatasets_V3.2"
    # train_all_out_path = "/home/david/Downloads/ShiLuoDeDatasets_V3.2//train_all.json"
    train_out_path = "E:\\code\Dataset\\ShiLuoDeDatasets_V3.2\\train.json"
    test_out_path = "E:\\code\Dataset\\ShiLuoDeDatasets_V3.2\\valid.json"
    annotations_path = os.path.join(root, "annotations")
    jsons_path = get_json_path(annotations_path)
    images_path = os.path.join(root, "normal")
    images_path = get_image_path(images_path)
    random.shuffle(jsons_path)
    random.shuffle(images_path)

    # train
    train_dataset = CreateCOCODataset(jsons_path[:880], images_path[:880])
    train_out = train_dataset.create_out()
    json.dump(train_out, open(train_out_path, 'w'))

    # test
    test_dataset = CreateCOCODataset(jsons_path[880:], images_path[880:])
    test_out = test_dataset.create_out()
    json.dump(test_out, open(test_out_path, 'w'))

    # train_all
    # train_all_dataset = CreateCOCODataset(jsons_path, images_path)
    #  train_all_out = train_all_dataset.create_out()
    #  json.dump(train_all_out, open(train_all_out_path, 'w'))
