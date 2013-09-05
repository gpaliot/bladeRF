#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <pthread.h>
#include <libbladeRF.h>

#include "repeater.h"

struct buf_mgmt
{
    void *rx;           /* Next buffer to RX into */
    void *tx;           /* Next buffer to TX from */
    size_t num_filled;  /* Number of buffers filled with RX data awaiting TX */

    pthread_mutex_t lock;

    /* Used to signal the TX thread when a few samplse have been buffered up */
    pthread_cond_t  samples_available;
}

struct repeater
{
    struct bladerf *device;

    pthread_t rx_task;
    struct bladerf_stream *rx_stream;

    pthread_t tx_task;
    struct bladerf_stream *tx_stream;

    void **buffers;
    void *buffer_end
    struct buf_mgmt buffers_mgmt;
};

void repeater_config_init(struct repeater_config *c)
{
    c->device_str = NULL;

    c->tx_freq = DEFAULT_FREQUENCY;
    c->rx_freq = DEFAULT_FREQUENCY;
    c->sample_rate = DEFAULT_SAMPLE_RATE;

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

static void *tx_stream_callback(struct bladerf *dev,
                                struct bladerf_stream *stream,
                                struct bladerf_metadata *meta,
                                void *samples,
                                size_t num_samples,
                                void *user_data)
{
    return NULL;
}

static void *rx_stream_callback(struct bladerf *dev,
                                struct bladerf_stream *stream,
                                struct bladerf_metadata *meta,
                                void *samples,
                                size_t num_samples,
                                void *user_data)
{
    return NULL;
}

static inline void repeater_init(struct repeater *repeater)
{
    memset(repeater, 0, sizeof(*repeater));
    pthread_mutex_init(&repeater->buffers_mgmt.lock);
}

static int init_device(struct repeater *repeater, struct repeater_config *config)
{
    int status;
    unsigned int sample_rate_actual;

    status = bladerf_open(&repeater->device, config->device_str);
    if (!repeater->device) {
        fprintf(stderr, "Failed to open %s: %s\n", config->device_str,
                bladerf_strerror(status));
        return -1;
    }

    status = bladerf_is_fpga_configured(repeater->device);
    if (status < 0) {
        fprintf(stderr, "Failed to determine if FPGA is loaded: %s\n",
                bladerf_strerror(status));
        goto init_device_error;
    } else if (status == 0) {
        fprintf(stderr, "FPGA is not loaded. Aborting.\n");
        status = BLADERF_ERR_NODEV;
        goto init_device_error;
    }

    status = bladerf_set_sample_rate(repeater->device, BLADERF_MODULE_TX,
                                     config->sample_rate, &sample_rate_actual);

    if (status < 0) {
        fprintf(stderr, "Failed to set TX sample rate: %s\n",
                bladerf_strerror(status));
        goto init_device_error;
    } else {
        printf("Actual TX sample rate is %d Hz\n", sample_rate_actual);
    }

    status = bladerf_set_sample_rate(repeater->device, BLADERF_MODULE_RX,
                                     config->sample_rate, &sample_rate_actual);

    if (status < 0) {
        fprintf(stderr, "Failed to set RX sample rate: %s\n",
                bladerf_strerror(status));
        goto init_device_error;
    } else {
        printf("Actual RX sample rate is %d Hz\n", sample_rate_actual);
    }

    status = bladerf_set_frequency(repeater->device,
                                   BLADERF_MODULE_TX, config->tx_freq);
    if (status < 0) {
        fprintf(stderr, "Failed to set TX frequency: %s\n",
                bladerf_strerror(status));
        goto init_device_error;
    } else {
        printf("Set TX frequency to %d Hz\n", config->tx_freq);
    }

    status = bladerf_set_frequency(repeater->device,
                                   BLADERF_MODULE_RX, config->rx_freq);
    if (status < 0) {
        fprintf(stderr, "Failed to set RX frequency: %s\n",
                bladerf_strerror(status));
        goto init_device_error;
    } else {
        printf("Set RX frequency to %d Hz\n", config->rx_freq);
    }

    return status;

init_device_error:
    bladerf_close(repeater->device);
    repeater->device = NULL;

    return status;
}

static void deinit(struct repeater *repeater)
{
    if (repeater->device) {
        if (repeater->rx_stream) {
            bladerf_deinit_stream(repeater->rx_stream);
        }

        if (repeater->tx_stream) {
            bladerf_deinit_stream(repeater->tx_stream);
        }

        bladerf_close(repeater->device);
        repeater->device = NULL;
    }
}

static int init_streams(struct repeater *repeater,
                        struct repeater_config *config)
{
    int status;

    /* TODO Until we can provide NULL to "user buffers", we'll just allocate
     *      some dummy buffers */
    void **dummy;

    status = bladerf_init_stream(&repeater->rx_stream,
                                 repeater->device,
                                 rx_stream_callback,
                                 &repeater->buffers,
                                 config->num_buffers,
                                 BLADERF_FORMAT_SC16_Q12,
                                 config->samples_per_buffer,
                                 config->num_transfers,
                                 repeater);
    if (status < 0) {
        fprintf(stderr, "Failed to initialize RX stream: %s\n",
                bladerf_strerror(status));
        return status;
    }


    status = bladerf_init_stream(&repeater->tx_stream,
                                 repeater->device,
                                 tx_stream_callback,
                                 &dummy,
                                 config->num_buffers,
                                 BLADERF_FORMAT_SC16_Q12,
                                 config->samples_per_buffer,
                                 config->num_transfers,
                                 repeater);
    if (status < 0) {
        fprintf(stderr, "Failed to initialize TX stream: %s\n",
                bladerf_strerror(status));
        return status;
    }

    return 0;
}

int repeater_run(struct repeater_config *config)
{
    int status;
    struct repeater repeater;

    repeater_init(&repeater);

    /* Configure the bladeRF */
    status = init_device(&repeater, config);
    if (status < 0) {
        goto repeater_run_end;
    }

    /* Allocate streams */
    status = init_streams(&repeater, config);
    if (status < 0) {
        goto repeater_run_end;
    }


    /* And start tasks */

repeater_run_end:
    deinit(&repeater);
    return 0;
}
