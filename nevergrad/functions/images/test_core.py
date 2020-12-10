# Copyright (c) Facebook, Inc. and its affiliates. All Rights Reserved.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import numpy as np
from nevergrad.functions.images import imagelosses

from . import core


def test_images_adversarial() -> None:
    func = next(core.ImageAdversarial.make_folder_functions(None, model="test"))
    x = np.zeros(func.image.shape)
    value = func(x)
    assert value < np.inf
    other_func = func.copy().copy()
    value2 = other_func(x)
    assert value2 == value  # same function


def test_image_adversarial_eval() -> None:
    func = next(core.ImageAdversarial.make_folder_functions(None, model="test"))
    output = func.evaluation_function(func.parametrization.value)
    assert output == 0
    func.targeted = True
    output = func.evaluation_function(func.parametrization.value)
    assert output == 1


def test_images() -> None:
    func = core.Image()
    x = 7 * np.fabs(np.random.normal(size=func.domain_shape))
    # data = func.parametrization.spawn_child().set_standardized_data(x.flatten()).value
    value = func(x)  # should not touch boundaries, so value should be < np.inf
    assert value < np.inf
    other_func = func.copy()
    value2 = other_func(x)
    assert value == value2


def test_image_from_pgan_with_l1_loss() -> None:
    func = core.ImageFromPGAN(initial_noise=None, use_gpu=False, loss=imagelosses.SumAbsoluteDifferences(reference=np.zeros((1, 512, 512, 3))))
    x = 7 * np.fabs(np.random.normal(size=func.noise_shape))
    value = func(x)  # should not touch boundaries, so value should be < np.inf
    assert value < np.inf
    other_func = func.copy()
    value2 = other_func(x)
    assert value == value2