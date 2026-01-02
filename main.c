#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <pthread.h>
#include <unistd.h>
#include "OS_header.h"
Job* job_queue[QUEUE_SIZE];
int count = 0;
int in = 0;
int out = 0;
int running = 1;
pthread_mutex_t mutex;
pthread_cond_t full_cond;
pthread_cond_t empty_cond;
void parse_command(char *input, Job *job) {
    int i = 0;
    char *token = strtok(input, " \n");
    while (token != NULL && i < 9) {
        job->args[i++] = token;
        token = strtok(NULL, " \n");
    }
    job->args[i] = NULL;
}
int main() {
    pthread_t tid;
    char input[CMD_LEN];
    int id_counter = 100;
    pthread_mutex_init(&mutex, NULL);
    pthread_cond_init(&full_cond, NULL);
    pthread_cond_init(&empty_cond, NULL);
    pthread_create(&tid, NULL, scheduler_thread, NULL);
    system("clear");
    printf("==================================================\n");
    printf("   OS SIMULATOR - MODULAR VERSION (Fall 2025)     \n");
    printf("==================================================\n");
    printf("Type commands (e.g., 'ls', 'date', 'pwd'). Type 'exit' to quit.\n\n");
    while(1) {
        printf("\033[1;34mUser@OS-Sim:~$ \033[0m"); 
        if (fgets(input, CMD_LEN, stdin) == NULL) break;
        input[strcspn(input, "\n")] = 0;
        if(strcmp(input, "exit") == 0) {
            running = 0;
            pthread_cond_signal(&full_cond);
            break;
        }
        if(strlen(input) == 0) continue;
        Job* new_job = (Job*)malloc(sizeof(Job));
        if (new_job == NULL) { perror("Malloc failed"); continue; }
        new_job->process_id = id_counter++;
        strcpy(new_job->command, input);
        parse_command(input, new_job);
        pthread_mutex_lock(&mutex);
        while(count == QUEUE_SIZE) {
            printf("[Shell] Queue Full! Waiting...\n");
            pthread_cond_wait(&empty_cond, &mutex);
        }
        job_queue[in] = new_job;
        in = (in + 1) % QUEUE_SIZE;
        count++;
        printf("[Shell] Process Created & Added to Queue. (ID: %d)\n", new_job->process_id);
        pthread_cond_signal(&full_cond);
        pthread_mutex_unlock(&mutex);
        sleep(1); 
    }
    pthread_join(tid, NULL);
    pthread_mutex_destroy(&mutex);
    pthread_cond_destroy(&full_cond);
    pthread_cond_destroy(&empty_cond);
    printf("System Shutdown Successfully.\n");
    return 0;
}