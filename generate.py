#coming soon

import os
from dataset import CustomDatasetDataLoader
import importlib
import argparse

def create_dataset(opt):
    data_loader = CustomDatasetDataLoader(opt)
    dataset = data_loader.load_data()
    return dataset

def create_model(opt):
    model_name = opt.model
    model_filename = "models." + model_name + "_model"
    modellib = importlib.import_module(model_filename)
    model = None
    target_model_name = model_name.replace('_', '') + 'model'
    for name, cls in modellib.__dict__.items():
        if name.lower() == target_model_name.lower() \
           and issubclass(cls, BaseModel):
            model = cls

    if model is None:
        print("In %s.py, there should be a subclass of BaseModel with class name that matches %s in lowercase." % (model_filename, target_model_name))
        exit(0)
    instance = model(opt)
    print("model [%s] was created" % type(instance).__name__)
    return instance
    

def save_images(opt):
    return True

if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--results_dir', type=str, default='./results/', help='saves results here.')
    parser.add_argument('--aspect_ratio', type=float, default=1.0, help='aspect ratio of result images')
    parser.add_argument('--phase', type=str, default='test', help='train, val, test, etc')
    # Dropout and Batchnorm has different behavioir during training and test.
    parser.add_argument('--eval', action='store_true', help='use eval mode during test time.')
    parser.add_argument('--num_test', type=int, default=50, help='how many test images to run')
    parser.add_argument('--meta_file', type=str, default='test', help='how many test images to run')
    # rewrite devalue values
    parser.set_defaults(model='test')
    # To avoid cropping, the load_size should be the same as crop_size
    parser.set_defaults(load_size=parser.get_default('crop_size'))

    opt = parser.parse_args()  # get test options
    # hard-code some parameters for test
    opt.num_threads = 0   # test code only supports num_threads = 1
    opt.batch_size = 1    # test code only supports batch_size = 1
    opt.serial_batches = True  # disable data shuffling; comment this line if results on randomly chosen images are needed.
    opt.no_flip = True    # no flip; comment this line if results on flipped images are needed.
    opt.display_id = -1   # no visdom display; the test code saves the results to a HTML file.
    dataset = create_dataset(opt)  # create a dataset given opt.dataset_mode and other options
    model = create_model(opt)      # create a model given opt.model and other options
    model.setup(opt)               # regular setup: load and print networks; create schedulers
    # # create a website
    # web_dir = os.path.join(opt.results_dir, opt.name, '{}_{}'.format(opt.phase, opt.epoch))  # define the website directory
    # if opt.load_iter > 0:  # load_iter is 0 by default
    #     web_dir = '{:s}_iter{:d}'.format(web_dir, opt.load_iter)
    # print('creating web directory', web_dir)
    # webpage = html.HTML(web_dir, 'Experiment = %s, Phase = %s, Epoch = %s' % (opt.name, opt.phase, opt.epoch))
    # # test with eval mode. This only affects layers like batchnorm and dropout.
    # # For [pix2pix]: we use batchnorm and dropout in the original pix2pix. You can experiment it with and without eval() mode.
    # # For [CycleGAN]: It should not affect CycleGAN as CycleGAN uses instancenorm without dropout.
    # if opt.eval:
    #     model.eval()
    # for i, data in enumerate(dataset):
    #     if i >= opt.num_test:  # only apply our model to opt.num_test images.
    #         break
    #     model.set_input(data)  # unpack data from data loader
    #     model.test()           # run inference
    #     visuals = model.get_current_visuals()  # get image results
    #     img_path = model.get_image_paths()     # get image paths
    #     if i % 5 == 0:  # save images to an HTML file
    #         print('processing (%04d)-th image... %s' % (i, img_path))
    #     save_images(webpage, visuals, img_path, aspect_ratio=opt.aspect_ratio, width=opt.display_winsize)
    # webpage.save()  # save the HTML
