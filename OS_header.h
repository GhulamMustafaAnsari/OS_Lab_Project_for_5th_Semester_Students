#ifndef OS_HEADER_H
#define OS_HEADER_H
#include <pthread.h>
#define QUEUE_SIZE 5
#define CMD_LEN 100
typedef struct {
    int process_id;
    char command[CMD_LEN];
    char *args[10];
} Job;
extern Job* job_queue[QUEUE_SIZE];
extern int count;
extern int in;
extern int out;
extern int running;
extern pthread_mutex_t mutex;
extern pthread_cond_t full_cond;
extern pthread_cond_t empty_cond;
void* scheduler_thread(void* arg);
void parse_command(char *input, Job *job);
#endif