/*
 * This test implements a simple full-duplex repeater.
 *
 * This file handles command line processing and passes control off to the
 * repeater.c file.
 */

#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <stdbool.h>
#include <limits.h>
#include <getopt.h>
#include <libbladeRF.h>
#include "conversions.h"    /* Conversion routines from host/common */
#include "repeater.h"

#define OPTARG_STR "d:s:t:r:S:B:T:h"

static struct option long_options[] = {
    { "device",         required_argument,  0,  'd'},
    { "samplerate",     required_argument,  0,  's'},
    { "tx-freq",        required_argument,  0,  't'},
    { "rx-freq",        required_argument,  0,  'r'},
    { "num-samples",    required_argument,  0,  'S'},
    { "num-buffers",    required_argument,  0,  'B'},
    { "num-transfers",  required_argument,  0,  'T'},
    { "verbosity",      required_argument,  0,  'v'},
    { "help",           no_argument,        0,  'h'},
    { 0,                0,                  0,  0},
};


static void usage(const char *argv0)
{
    printf("Simple full duplex repeater test\n\n");
    printf("Usage: %s [options]\n\n", argv0);
    printf("  -d, --device  <device>    Device to use. If not specified, the\n"
           "                            first device found will be used.\n\n");

    printf("  -s, --samplerate <rate>   Sample rate in Hz. Default is %d\n\n",
                                        DEFAULT_SAMPLE_RATE);

    printf("  -t, --tx-freq <freq>      Transmit frequency, in Hz. Default is %d\n\n",
                                        DEFAULT_FREQUENCY);

    printf("  -r, --rx-freq <freq>      Receive frequency, in Hz. Default is %d\n\n",
                                        DEFAULT_FREQUENCY);

    printf("  -S, --num-samples <n>     Number of samples per buffer. Default is %d.\n"
           "                            Must be a multiple of 1024.\n\n",
                                        DEFAULT_SAMPLES_PER_BUFFER);

    printf("  -B, --num-buffers <n>     Number of buffers to use. Default is %d\n\n",
                                        DEFAULT_NUM_BUFFERS);

    printf("  -T, --num-transfers <n>   Number of transfers to use. Default is %d.\n"
           "                            This value should be less than the\n"
           "                            number of buffers being used.\n\n",
                                        DEFAULT_NUM_TRANSFERS);

    printf("  -v, --verbosity <level>   Set libbladeRF verbosity level.\n\n");

    printf("  -h, --help                Show this text\n\n");
}

static int handle_args(int argc, char *argv[], struct repeater_config *config)
{
    int opt, opt_idx;
    bool conv_ok;

    repeater_config_init(config);

    opt = getopt_long(argc, argv, OPTARG_STR, long_options, &opt_idx);
    while (opt != -1) {
        switch(opt) {
            case 'd':
                if (!config->device_str) {
                    config->device_str = strdup(optarg);
                    if (!config->device_str) {
                        perror("strdup");
                        return -1;
                    }
                } else {
                    fprintf(stderr, "Device already specified: %s",
                            config->device_str);
                    return -1;
                }
                break;

            case 't':
                config->tx_freq = str2int(optarg, 1, INT_MAX, &conv_ok);
                if (!conv_ok) {
                    fprintf(stderr, "Invalid TX frequency: %d\n",
                            config->tx_freq);
                    return -1;
                }
                break;

            case 'r':
                config->rx_freq = str2int(optarg, 1, INT_MAX, &conv_ok);
                if (!conv_ok) {
                    fprintf(stderr, "Invalid RX frequency: %d\n",
                            config->rx_freq);
                    return -1;
                }
                break;

            case 's':
                config->sample_rate = str2int(optarg, 1, INT_MAX, &conv_ok);
                if (!conv_ok) {
                    fprintf(stderr, "Invalid sample rate: %d\n",
                            config->sample_rate);
                }
                break;

            case 'S':
                config->samples_per_buffer =
                        str2int(optarg, 1024, INT_MAX, &conv_ok);

                if (!conv_ok || config->samples_per_buffer % 1024 != 0) {
                    fprintf(stderr, "Invalid samples value: %d\n",
                            config->samples_per_buffer);
                    return -1;
                }
                break;

            case 'B':
                config->num_buffers = str2int(optarg, 1, INT_MAX, &conv_ok);
                if (!conv_ok) {
                    fprintf(stderr, "Invalid number of buffers: %d\n",
                            config->num_buffers);
                    return -1;
                }
                break;

            case 'T':
                config->num_transfers = str2int(optarg, 1, INT_MAX, &conv_ok);
                if (!conv_ok) {
                    fprintf(stderr, "Invalid number of transfers: %d\n",
                            config->num_buffers);
                    return -1;
                }
                break;

            case 'v':
                if (!strcasecmp(optarg, "critical")) {
                    config->verbosity = BLADERF_LOG_LEVEL_CRITICAL;
                } else if (!strcasecmp(optarg, "error")) {
                    config->verbosity = BLADERF_LOG_LEVEL_ERROR;
                } else if (!strcasecmp(optarg, "warning")) {
                    config->verbosity = BLADERF_LOG_LEVEL_WARNING;
                } else if (!strcasecmp(optarg, "info")) {
                    config->verbosity = BLADERF_LOG_LEVEL_INFO;
                } else if (!strcasecmp(optarg, "debug")) {
                    config->verbosity = BLADERF_LOG_LEVEL_DEBUG;
                } else if (!strcasecmp(optarg, "verbose")) {
                    config->verbosity = BLADERF_LOG_LEVEL_VERBOSE;
                } else {
                    fprintf(stderr, "Unknown verbosity level: %s\n", optarg);
                    return -1;
                }
                break;

            case 'h':
                return 1;
        }

        opt = getopt_long(argc, argv, "d:", long_options, &opt_idx);
    }

    if (config->samples_per_buffer < 1024 ||
        config->samples_per_buffer % 1024 != 0) {
        fprintf(stderr, "# samples must be >= 1024 and a multiple of 1024\n");
        return -1;
    }

    return 0;
}



int main(int argc, char *argv[])
{
    int status;
    struct repeater_config config;

    status = handle_args(argc, argv, &config);
    if (!status) {
        status = repeater_run(&config);
    } else {
        usage(argv[0]);
    }

    repeater_config_deinit(&config);
    return status;
}
