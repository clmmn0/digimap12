import os
import argparse
import tensorflow.compat.v1 as tf
import model

FLAGS = tf.app.flags.FLAGS
tf.compat.v1.disable_v2_behavior()

def parse_args():
    parser = argparse.ArgumentParser(description='deblur arguments')
    parser.add_argument('--gpu', type=str, default='0', 
                        help='set gpu id or leave it blank for cpu')
    parser.add_argument('--model', type=str, default='default', 
                        help='choose the model trained on default data or all data')
    parser.add_argument('--input_path', type=str, default='./static/images/input_images',
                        help='path of testing folder or path of one testing image')
    parser.add_argument('--max_height', type=int, default=720,
                        help='max height for the input tensor, should be multiples of 16')
    parser.add_argument('--max_width', type=int, default=1280,
                        help='max width for the input tensor, should be multiples of 16')
    args = parser.parse_args()
    return args


def main(_):
    args = parse_args()

    # set gpu id or leave it blank for cpu
    if args.gpu == 'cpu':
        os.environ['CUDA_VISIBLE_DEVICES'] = ''
    else:
        os.environ['CUDA_VISIBLE_DEVICES'] = args.gpu

    # choose the model trained on default data or all data
    if args.model == 'default':
        model_path = os.path.join('checkpoints', 'default')
    else:
        model_path = os.path.join('checkpoints', 'alldata')

    deblur = model.DEBLUR(args)
    deblur.build(model_path)
    deblur.test()

if __name__ == '__main__':
    tf.app.run(main)