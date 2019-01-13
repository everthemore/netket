# Copyright 2018 The Simons Foundation, Inc. - All Rights Reserved.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#    http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import netket as nk
from mpi4py import MPI
from ed import load_ed_data
import matplotlib.pyplot as plt
import numpy as np

L = 10

# Load the Hilbert space info and data
hi, training_samples, training_targets = load_ed_data(L)

# Machine
ma = nk.machine.RbmSpin(hilbert=hi, alpha=1)

ma.init_random_parameters(seed=1234, sigma=0.1)

# Sampler
sa = nk.sampler.MetropolisLocal(machine=ma)

# Optimizer
# op = nk.optimizer.Sgd(1e-1)
op = nk.optimizer.AdaDelta()


spvsd = nk.supervised.supervised(
    sampler=sa,
    optimizer=op,
    batch_size=1000,
    output_file="output",
    samples=training_samples,
    targets=training_targets)

niter = 500

overlaps = []

# Run with "Overlap" loss. Also available currently is "MSE"
for i in range(niter):
    spvsd.iterate(loss_function="Overlap_phi")
    print(spvsd.log_overlap.real)
    overlaps.append(np.exp(-spvsd.log_overlap.real))

plt.plot(overlaps)
plt.ylabel('Overlap')
plt.xlabel('Iteration #')
plt.axhline(y=1, xmin=0, xmax=niter, linewidth=2, color='k', label='1')
plt.title(r'Transverse-field Ising model, $L=' + str(L) + '$')
plt.show()