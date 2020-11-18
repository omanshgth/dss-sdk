/**
 *   BSD LICENSE
 *
 *   Copyright (c) 2019 Samsung Electronics Co., Ltd.
 *   All rights reserved.
 *
 *   Redistribution and use in source and binary forms, with or without
 *   modification, are permitted provided that the following conditions
 *   are met:
 *
 *     * Redistributions of source code must retain the above copyright
 *       notice, this list of conditions and the following disclaimer.
 *     * Redistributions in binary form must reproduce the above copyright
 *       notice, this list of conditions and the following disclaimer in
 *       the documentation and/or other materials provided with the
 *       distribution.
 *     * Neither the name of Samsung Electronics Co., Ltd. nor the names of
 *       its contributors may be used to endorse or promote products derived
 *       from this software without specific prior written permission.
 *
 *   THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
 *   "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
 *   LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
 *   A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
 *   OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
 *   SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
 *   LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
 *   DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
 *   THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 *   (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
 *   OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 */

#ifndef NKV_STRUCT_H
#define NKV_STRUCT_H
#include "nkv_const.h"

#ifdef __cplusplus
extern "C" {
#endif
#include <sys/time.h>

typedef struct {
  
  //Instance hosting node name or ip
  char* host_name_ip;
  //Instance end-point
  uint32_t host_port;
  // nkv instance uuid
  uint64_t instance_uuid;
  //Instance creation time
  time_t mtime;
  //NKV instance will be periodically updating this heart-beat time to let other instance know it is alive
  // this is mainly needed to override a lock if owner instance is crashed before unlocking. Following
  // attribute tells the duration in seconds last heart-beat updated
  uint64_t last_hb_duration;
} nkv_instance_info;

typedef struct {
  //Container transport path id , generated by NKV
  int32_t network_path_id;

  //Network path hash , generated by NKV
  uint64_t network_path_hash;

  // IP address of the path, length allocated should be NKV_MAX_IP_LENGTH
  char ip_addr[NKV_MAX_IP_LENGTH];

  //Path port
  int32_t port; 

  //Container transport family, 2 = ipv4 or 10 =ipv6
  int8_t addr_family; 

  //Container transport speed, 0 = 1Gb, 1 = 10Gb, 2 = 50Gb, 3 = 100Gb
  int8_t speed; 

  //Container transport status, 0 = Down , 1 = Up
  int8_t status;

  //Container transport aligned to numanode#
  int8_t numa_node;

  //Mount point of the path, length allocated should be NKV_MAX_MOUNT_POINT_LENGTH
  char mount_point[NKV_MAX_MOUNT_POINT_LENGTH];


} nkv_container_transport;

typedef struct {

  // ID of the container
  uint32_t container_id;

  // Hash ID of the container, generated by NKV
  uint64_t container_hash;

  // UUID of the container, length allocated should be NKV_MAX_CONT_NAME_LENGTH
  char container_uuid[NKV_MAX_CONT_NAME_LENGTH];

  // Name of the container, length allocated should be NKV_MAX_CONT_NAME_LENGTH                                              
  char container_name[NKV_MAX_CONT_NAME_LENGTH];    

  // Physical target node hosting the container, length allocated should be NKV_MAX_CONT_NAME_LENGTH                            
  char hosting_target_name[NKV_MAX_CONT_NAME_LENGTH];   

  //Container status, OK, DOWN                        
  uint8_t container_status;    

  //Percentage space available on the container                     
  uint8_t container_space_available_percentage; 

  // IN/OUT, number of nkv_container_transport* allocated, IN should be NKV_MAX_CONT_TRANSPORT
  int8_t num_container_transport;   

  // Container transport details
  nkv_container_transport* transport_list; 

} nkv_container_info;

typedef struct { 

  void *key; 
  uint32_t length;
 
} nkv_key;

typedef struct {

  //The value buffer allocated by user
  void *value;

  //The length of the value buffer in bytes
  uint64_t length;

  //The actual length of the key value object in bytes (valid for retrieve case)
  uint64_t actual_length;
 
} nkv_value; 

typedef struct { 

  int8_t nkv_store_compressed:1;
  int8_t nkv_store_ecrypted:1;
  int8_t nkv_store_crc_in_meta:1;
  int8_t nkv_store_no_overwrite:1;
  int8_t nkv_store_atomic:1;
  int8_t nkv_store_update_only:1;
  int8_t nkv_store_append:1;

} nkv_store_option;

typedef struct {

  int8_t nkv_retrieve_decompress:1;
  int8_t nkv_retrieve_decrypt:1;
  int8_t nkv_compare_crc:1;
  int8_t nkv_retrieve_delete:1;

} nkv_retrieve_option;

typedef struct {
  int8_t nkv_lock_priority:2;
  int8_t nkv_lock_writer:1;
  int8_t nkv_lock_blocking:1;
  uint32_t nkv_lock_duration;
  uint64_t nkv_lock_uuid;
}nkv_lock_option;

typedef nkv_lock_option nkv_unlock_option;

typedef struct {

  //Using NKV in pass-through mode ? 0 – non-pass-through, 1 – pass-through
  int8_t is_pass_through;

  //Hash id of the physical container, needed for pass-through mode
  uint64_t container_hash;

  //Container transport path hash, not needed if nic_load_balance and nic_failover feature is enabled
  //optional for listing, if not supplied, make it 0.
  uint64_t network_path_hash;

  //NKV generated Key space Id, not needed for pass-through mode
  int32_t ks_id;

} nkv_io_context;

typedef struct {

  //Using NKV in pass-through mode ? 0 – non-pass-through, 1 – pass-through
  int8_t is_pass_through;

  //Hash id of the physical container, needed for pass-through mode
  uint64_t container_hash;

  //Container transport path hash, needed for pass-through mode
  uint64_t network_path_hash;

} nkv_mgmt_context;
  
typedef struct {

  char path_mount_point[NKV_MAX_MOUNT_POINT_LENGTH];
  uint64_t path_storage_capacity_in_bytes;
  uint64_t path_storage_usage_in_bytes;
  double   path_storage_util_percentage;

} nkv_path_stat; 

typedef struct {
	// Multipath Load Balance flag. 0 is disable, 1 is enable
	uint32_t nic_load_balance;
	
	// Multipath Load Balance plicy
	// 0 - Round Robin (default) 
	// 1 - Failover policy 
	// 2 - Least Queue Depth
	// 3 - Least Queue Size
	uint32_t nic_load_balance_policy;
	
} nkv_feature_list;

typedef struct {
 
  int32_t opcode; 	// operation code, 0 = GET, 1 = PUT, 2= DEL
  nkv_key key; 	        // pointer for a key data structure 
  nkv_value value; 	// pointer for a value data structure 
  int32_t result; 	// return value (results) 
  void *private_data_1; // private data address passed by caller
  void *private_data_2; // private data address passed by caller
	
} nkv_aio_construct;


typedef struct {
  //nkv_aio_construct structure containing key and value pair along with operation return value
  //num_op represents number of nkv_aio_construct structure returned. Only in case of batch  
  // operation it could be greater than 1.

  void (*nkv_aio_cb)(nkv_aio_construct* ops, int32_t num_op);

  //Application private data that application wants to get back with nkv_aio_cb
  void *private_data_1;
  void *private_data_2;
  
} nkv_postprocess_function;


typedef enum stat_type {
        STAT_TYPE_INT8,
        STAT_TYPE_INT16,
        STAT_TYPE_INT32,
        STAT_TYPE_INT64,
        STAT_TYPE_UINT8,
        STAT_TYPE_UINT16,
        STAT_TYPE_UINT32,
        STAT_TYPE_UINT64,
        STAT_TYPE_SIZE, /* uint64_t regardless of word size */
        STAT_TYPE_MAX
} nkv_stat_type_t;


typedef struct {
        const char *counter_name;
        nkv_stat_type_t counter_type;
} nkv_stat_counter;


#ifdef __cplusplus
} // extern "C"
#endif

#endif
