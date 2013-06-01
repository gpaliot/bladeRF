#include <stdlib.h>
#include <string.h>
#include <limits.h>
#include <fcntl.h>
#include <unistd.h>
#include <errno.h>
#include <dirent.h>
#include <sys/ioctl.h>

#include "bladerf.h"
#include "bladerf_priv.h"
#include "driver.h"
#include "debug.h"

#ifndef BLADERF_DEV_DIR
#   define BLADERF_DEV_DIR "/dev/"
#endif

#ifndef BLADERF_DEV_PFX
#   define BLADERF_DEV_PFX  "bladerf"
#endif

static int bladerf_filter(const struct dirent *d)
{
    const size_t pfx_len = strlen(BLADERF_DEV_PFX);
    long int tmp;
    char *endptr;

    if (strlen(d->d_name) > pfx_len &&
        !strncmp(d->d_name, BLADERF_DEV_PFX, pfx_len)) {

        /* Is the remainder of the entry a valid (positive) integer? */
        tmp = strtol(&d->d_name[pfx_len], &endptr, 10);

        /* Nope */
        if (*endptr != '\0' || tmp < 0 ||
            (errno == ERANGE && (tmp == LONG_MAX || tmp == LONG_MIN)))
            return 0;

        /* Looks like a bladeRF by name... we'll check more later. */
        return 1;
    }

    return 0;
}

static inline void free_dirents(struct dirent **d, int n)
{
    if (d && n > 0 ) {
        while (n--)
            free(d[n]);
        free(d);
    }
}

/* Open and if a non-NULL bladerf_devinfo ptr is provided, attempt to verify
 * that the device we opened is a bladeRF via a info calls.
 * (Does not fill out devinfo's path) */
struct bladerf * bladerf_open_(const char *dev_path,
                               struct bladerf_devinfo *i)
{
    struct bladerf *ret;

    ret = malloc(sizeof(*ret));
    if (!ret)
        return NULL;

    /* TODO -- spit out error/warning message to assist in debugging
     * device node permissions issues?
     */
    if ((ret->fd = open(dev_path, O_RDWR)) < 0)
        goto bladerf_open__err;

    /* TODO -- spit our errors/warning here depending on library verbosity? */
    if (i) {
        if (bladerf_get_serial(ret, &i->serial) < 0)
            goto bladerf_open__err;

        i->fpga_configured = bladerf_is_fpga_configured(ret);
        if (i->fpga_configured < 0)
            goto bladerf_open__err;

        if (bladerf_get_fw_version(ret, &i->fw_ver_maj, &i->fw_ver_min) < 0)
            goto bladerf_open__err;
    }

    return ret;

bladerf_open__err:
    free(ret);
    return NULL;
}

ssize_t bladerf_get_device_list(struct bladerf_devinfo **devices)
{
    struct bladerf_devinfo *ret;
    ssize_t num_devices;
    struct dirent **matches;
    int num_matches, i;
    struct bladerf *dev;
    char *dev_path;

    ret = NULL;
    num_devices = -1;

    num_matches = scandir(BLADERF_DEV_DIR, &matches, bladerf_filter, alphasort);
    if (num_matches > 0) {

        ret = malloc(num_matches * sizeof(*ret));
        if (!ret) {
            num_devices = BLADERF_ERR_MEM;
            goto bladerf_get_device_list_out;
        }

        num_devices = 0;
        for (i = 0; i < num_matches; i++) {
            dev_path = malloc(strlen(BLADERF_DEV_DIR) +
                                strlen(matches[i]->d_name) + 1);

            if (dev_path) {
                strcpy(dev_path, BLADERF_DEV_DIR);
                strcat(dev_path, matches[i]->d_name);

                dev = bladerf_open_(dev_path, &ret[num_devices]);

                if (dev) {
                    ret[num_devices++].path = dev_path;
                    bladerf_close(dev);
                } else
                    free(dev_path);
            }
        }
    }


bladerf_get_device_list_out:
    *devices = ret;
    free_dirents(matches, num_matches);
    return num_devices;
}

void bladerf_free_device_list(struct bladerf_devinfo *devices, size_t n)
{
    size_t i;

    if (devices) {
        for (i = 0; i < n; i++)
            free(devices[i].path);
        free(devices);
    }
}

struct bladerf * bladerf_open(const char *dev_path)
{
    struct bladerf_devinfo i;
    struct bladerf *ret;

    /* Use the device info to ensure what we opened is actually a bladeRF */
    ret = bladerf_open_(dev_path, &i);

    if (ret)
        free(i.path);

    return ret;
}

void bladerf_close(struct bladerf *dev)
{
    if (dev) {
        close(dev->fd);
        free(dev);
    }
}

int bladerf_set_loopback( struct bladerf *dev, enum bladerf_loopback l)
{
    return 0;
}

int bladerf_set_sample_rate(struct bladerf *dev, unsigned int rate)
{
    return 0;
}


int bladerf_set_txvga2(struct bladerf *dev, int gain)
{
    return 0;
}

int bladerf_set_txvga1(struct bladerf *dev, int gain)
{
    return 0;
}

int bladerf_set_lna_gain(struct bladerf *dev, enum bladerf_lna_gain gain)
{
    return 0;
}

int bladerf_set_rxvga1(struct bladerf *dev, int gain)
{
    return 0;
}

int bladerf_set_rxvga2(struct bladerf *dev, int gain)
{
    return 0;
}

int bladerf_set_bandwidth(struct bladerf *dev, unsigned int bandwidth,
                            unsigned int *bandwidth_actual)
{
    return 0;
}

int bladerf_set_frequency(struct bladerf *dev,
                            enum bladerf_module module, unsigned int frequency)
{
    return 0;
}

ssize_t bladerf_send_c12(struct bladerf *dev, int16_t *samples, size_t n)
{
    return 0;
}

ssize_t bladerf_send_c16(struct bladerf *dev, int16_t *samples, size_t n)
{
    return 0;
}

ssize_t bladerf_read_c16(struct bladerf *dev,
                            int16_t *samples, size_t max_samples)
{
    return 0;
}

int bladerf_get_serial(struct bladerf *dev, uint64_t *serial)
{
    *serial = 0;
    return 0;
}

int bladerf_is_fpga_configured(struct bladerf *dev)
{
    return 0;
}

int bladerf_get_fw_version(struct bladerf *dev,
                            unsigned int *major, unsigned int *minor)
{
    *major = 0;
    *minor = 1;
    return 0;
}