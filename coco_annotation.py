#-------------------------------------------------------#
#   用于处理COCO数据集，根据json文件生成txt文件用于训练
#-------------------------------------------------------#
import json
import os
from collections import defaultdict
import argparse


def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('--root-path', type=str, default='E:\\code\\dissertation\\yolox-pytorch',
                        help="point to your root path, which is related to your own computer set")
    parser.add_argument('--dataset-path', type=str, default='E:\\code\\Dataset\\ShiLuoDeDatasets_V3.2',
                        help="point to your dataset path, which is related to your dataset path")
    parser.add_argument('--train-annotation', type=str, default='annotations\\train.json',
                        help="point to your train annotations file, which is related to your annotations")
    parser.add_argument('--valid-annotation', type=str, default='annotations\\valid.json',
                        help="point to your valid annotations file, which is related to your annotations")
    parser.add_argument('--output-path', type=str, default='model_data\\txt_data\\',
                        help="point to your generated txt path")
    parser.add_argument('--train-file', type=str, default='train.txt', help="your output train txt file name")
    parser.add_argument('--valid-file', type=str, default='valid.txt', help="your output valid txt file name")
    opt = parser.parse_args()
    return opt


def write_txt(input_anno_path, input_img_path, output_path):
    name_box_id = defaultdict(list)
    f = open(input_anno_path, encoding = 'utf-8')
    data = json.load(f)
    annotations = data['annotations']
    image = data['images']
    for img in image:
        image_id = img["id"]
        name = os.path.join(input_img_path, img['file_name'])
        no_defect = True
        for ant in annotations:
            ant_image_id = ant["image_id"]
            if ant_image_id == image_id:
                cat = ant['category_id'] - 1
                # cat = 0
                name_box_id[name].append([ant['bbox'], cat])
                no_defect = False
        if no_defect:
            name_box_id[name].append([])

    f = open(output_path, 'w')
    for key in name_box_id.keys():
        f.write(key)
        box_infos = name_box_id[key]
        if box_infos == [[]]:
            pass
        else:
            for info in box_infos:
                x_min = int(info[0][0])
                y_min = int(info[0][1])
                x_max = x_min + int(info[0][2])
                y_max = y_min + int(info[0][3])
                box_info = " %d,%d,%d,%d,%d" % (
                    x_min, y_min, x_max, y_max, int(info[1]))
                f.write(box_info)
        f.write('\n')
    f.close()


if __name__ == "__main__":
    opt = parse_opt()
    train_annotation_path = os.path.join(opt.dataset_path, opt.train_annotation)
    val_annotation_path = os.path.join(opt.dataset_path, opt.valid_annotation)
    train_output_path = os.path.join(opt.root_path, opt.output_path, opt.train_file)
    val_output_path = os.path.join(opt.root_path, opt.output_path, opt.valid_file)

    write_txt(train_annotation_path, opt.dataset_path, train_output_path)
    print('写入训练集标注文件成功')

    write_txt(val_annotation_path, opt.dataset_path, val_output_path)
    print('写入验证集标注文件成功')