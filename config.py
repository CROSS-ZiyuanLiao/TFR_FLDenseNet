from pprint import pprint
from pprint import pformat
import os
import logging


class Config:
    # data
    data_dir = ' '
    test_data_dir = None
    out_pred_dir = '/home/zhtang/waterLZY/txt/'
    test_data_name = None
    out = 'predict'

    num_of_samples = 'default'

    nets = ['waternetsmallfl', 'watercnndsnetf_in4_out58', 'waterdsnetf_in4_out58', 'waterdsnetf_self_define']

    # pretrained
    pretrained = None

    # architecture of network
    customize = True
    arch = 'waternet'
    growth_rate = 128
    num_init_features = 1536
    num_classes = 12

    multi_label = 1

    train_num_workers = 4
    test_num_workers = 4

    # optimizers
    optim = 'SGD'
    use_adam = False

    # param for optimizer
    # lr = {}
    # weight_decay = {}
    # lr_decay = {}

    # lr['waterdsnetf_self_define'] = 0.6
    # weight_decay['waterdsnetf_self_define'] = 0.00005
    # lr_decay['waterdsnetf_self_define'] = 0.33

    # lr['waternetsmallfl'] = 0.01
    # weight_decay['waternetsmallfl'] = 0.00005
    # lr_decay['waternetsmallfl'] = 0.33

    # lr['watercnndsnetf_in4_out58'] = 0.1
    # weight_decay['watercnndsnetf_in4_out58'] = 0.00005
    # lr_decay['watercnndsnetf_in4_out58'] = 0.33

    # lr['waterdsnetf_in4_out58'] = 0.2
    # weight_decay['waterdsnetf_in4_out58'] = 0.00005
    # lr_decay['waterdsnetf_in4_out58'] = 0.33
    logging_name = 'log'
    predict_name = '_predict.txt'
    activation = 'relu'

    lr = 0.6
    weight_decay = 0.00005
    lr_decay = 0.33  #

    # record i-th log
    kind = '0'

    # set gpu :
    # gpu = True

    # visualization
    env = 'water-nn'  # visdom env
    port = 8097
    plot_every = 40  # vis every N iter

    # preset
    data = 'water'

    # training
    epoch = 120

    # if eval
    evaluate = False

    test_num = 10000

    # model
    load_path = None
    save_path = '~/water/modelparams'

    # len(labels_dict) == 12
    labels_dict_12 = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12
    )

    # len(labels_dict) == 58
    labels_dict_58 = (379, 385, 390, 391, 392, 406, 414, 415, 416, 417, 418, 419, 420, 422,
    425, 434, 435, 436, 438, 439, 440, 441, 443, 444, 445, 446, 447, 448, 449,
    450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 464, 465, 466, 468, 512,
    513, 514, 515, 517, 518, 519, 520, 557, 558, 559, 560, 561, 562
    )
    labels_dict = ()

    def _parse(self, kwargs):
        state_dict = self._state_dict()
        for k, v in kwargs.items():
            if k not in state_dict:
                raise ValueError('UnKnown Option: "--%s"' % k)
            setattr(self, k, v)

        if opt.customize:
            self.logging_name = self.logging_name + '_self_' + opt.arch + '_'+ opt.optim + opt.kind + '_lr_' + str(self.lr)
        else:
            self.logging_name = self.logging_name + '_default_' + opt.arch  + '_' + opt.optim + opt.kind + '_lr_' + str(self.lr)

        print('======user config========')
        pprint(self._state_dict())
        print('==========end============')

        if opt.multi_label > 1:
            self.multi_label = opt.multi_label
            self.logging_name = self.logging_name + '_multi_label_' + str(self.multi_label)

        if not os.path.exists('log'):
            os.mkdir('log')

        if opt.arch == 'waterdsnetf':
            self.labels_dict = self.labels_dict_12
        elif opt.arch == 'waterdsnetf_in4_out58':
            self.labels_dict = self.labels_dict_58
        elif opt.arch == 'waterdsnetf_self_define':
            self.labels_dict = self.labels_dict_12
        elif opt.arch == 'watercnndsnetf_in4_out58':
            self.labels_dict = self.labels_dict_58
        elif opt.arch == 'waternetsmallfl':
            self.labels_dict = self.labels_dict_58

        if self.test_data_dir:
            # self.logging_name = self.logging_name + '_TestWith_' + self.test_data_name
            pass
        else:
            pass

        if self.num_of_samples == 'default':
            self.logging_name = self.logging_name + '_num_of_samples_' + self.num_of_samples
        else:
            self.logging_name = self.logging_name + '_num_of_samples_' + str(self.num_of_samples)

        self.predict_name = self.logging_name + self.predict_name
        self.logging_name = self.logging_name + '.log'

        logging_path = os.path.join('log', self.logging_name)
        print(self.logging_name)

        logging.basicConfig(level=logging.DEBUG,
                        filename=logging_path,
                        filemode='a',
                        format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                        datefmt='%H:%M:%S')
        logging.info('Logging for {}'.format(opt.arch))
        logging.info('======user config========')
        logging.info(pformat(self._state_dict()))
        logging.info('==========end============')
        # logging.info('optim : [{}], batch_size = {}, lr = {}, weight_decay= {}, momentum = {}'.format( \
        #                 args.optim, args.batch_size,
        #                 args.lr, args.weight_decay, args.momentum) )

    def _state_dict(self):
        return {k: getattr(self, k) for k, _ in Config.__dict__.items() \
                if not k.startswith('_')}


opt = Config()
