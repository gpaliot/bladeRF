#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <pthread.h>
#include <libbladeRF.h>

#include "repeater.h"

struct task
{
    pthread_t thread;

    void **buffers;
    int num_buffers;

    pthread_mutex_t *buffers_lock;
};

static int init_tasks(struct task *rx_task, struct task *tx_task)
{
    return 0;
}


void repeater_config_init(struct repeater_config *c)
{
    c->device_str = NULL;

    c->num_buffers = DEFAULT_NUM_BUFFERS;
    c->num_transfers = DEFAULT_NUM_TRANSFERS;
    c->samples_per_buffer = DEFAULT_SAMPLES_PER_BUFFER;

    c->verbosity = BLADERF_LOG_LEVEL_INFO;
}

void repeater_config_deinit(struct repeater_config *c)
{
    free(c->device_str);
    c->device_str = NULL;
}

int repeater_init(struct repeater_config *config, struct bladerf **device,
                  struct task *rx_task, struct task *tx_task)
{
    return 0;
}

int repeater_run(struct repeater_config *c)
{
    int status;
    struct task rx_task, tx_task;
    struct bladerf *device;

    status = bladerf_open(&device, c->device_str);

    if (!device) {
        fprintf(stderr, "Failed to open %s: %s\n", c->device_str,
                bladerf_strerror(status));
        return -1;
    }

    status = init_tasks(&rx_task, &tx_task);


    bladerf_close(device);

    return 0;
}
