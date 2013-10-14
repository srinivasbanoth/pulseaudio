#ifndef foopulsedomainhfoo
#define foopulsedomainhfoo

/***
  This file is part of PulseAudio.

  Copyright (c) 2012 Intel Corporation
  Janos Kovacs <jankovac503@gmail.com>

  PulseAudio is free software; you can redistribute it and/or modify
  it under the terms of the GNU Lesser General Public License as published
  by the Free Software Foundation; either version 2.1 of the License,
  or (at your option) any later version.

  PulseAudio is distributed in the hope that it will be useful, but
  WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
  General Public License for more details.

  You should have received a copy of the GNU Lesser General Public License
  along with PulseAudio; if not, write to the Free Software
  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307
  USA.
***/

#define PA_PULSE_DOMAIN_NAME "Pulse"

typedef struct pa_pulse_domain pa_pulse_domain;
typedef struct pa_pulse_domain_node_data pa_pulse_domain_node_data;

/* Forward declarations for external structs. */
typedef struct pa_core pa_core;
typedef struct pa_domain pa_domain;

struct pa_pulse_domain {
    pa_domain *domain;
};

typedef enum {
    PA_PULSE_DOMAIN_NODE_TYPE_PORT,
    PA_PULSE_DOMAIN_NODE_TYPE_SINK,
    PA_PULSE_DOMAIN_NODE_TYPE_SOURCE,
    PA_PULSE_DOMAIN_NODE_TYPE_SINK_INPUT,
    PA_PULSE_DOMAIN_NODE_TYPE_SOURCE_OUTPUT
} pa_pulse_domain_node_type_t;

struct pa_pulse_domain_node_data {
    pa_pulse_domain_node_type_t type;
    void *owner;
};

const char *pa_pulse_domain_node_type_to_string(pa_pulse_domain_node_type_t type);

pa_pulse_domain *pa_pulse_domain_new(pa_core *core);
void pa_pulse_domain_free(pa_pulse_domain *pulse_domain);

pa_pulse_domain_node_data *pa_pulse_domain_node_data_new(pa_pulse_domain_node_type_t type, void *owner);
void pa_pulse_domain_node_data_free(pa_pulse_domain_node_data *data);

#endif
