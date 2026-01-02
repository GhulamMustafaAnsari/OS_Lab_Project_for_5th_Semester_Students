#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>
#include "OS_header.h"
void* scheduler_thread(void* arg) {
    printf("[Kernel] Scheduler Module Loaded...\n");
    while(running) {
        pthread_mutex_lock(&mutex);
        while(count == 0 && running) {
            pthread_cond_wait(&full_cond, &mutex);
        }
        if (!running && count == 0) {
            pthread_mutex_unlock(&mutex);
            break;
        }
        Job* current_job = job_queue[out];
        out = (out + 1) % QUEUE_SIZE;
        count--;
        printf("\n\033[0;32m[Scheduler] Dispatching Process ID: %d | Command: %s\033[0m\n", 
               current_job->process_id, current_job->args[0]);
        pthread_cond_signal(&empty_cond);
        pthread_mutex_unlock(&mutex);
        pid_t pid = fork();
        if (pid < 0) {
            perror("Fork failed");
        } 
        else if (pid == 0) {
            if (execvp(current_job->args[0], current_job->args) < 0) {
                perror("Execution failed");
            }
            exit(0);
        } 
        else {
            wait(NULL);
            printf("[Scheduler] Process ID: %d Completed.\n", current_job->process_id);
        }
        free(current_job); 
        sleep(1);
    }
    printf("[Kernel] Scheduler Thread Stopped.\n");
    return NULL;
}