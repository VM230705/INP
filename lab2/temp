#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <sys/stat.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <fcntl.h>
#include <unistd.h>
#include <string>

using namespace std;

typedef struct {
        char magic[4];
        int32_t  off_str;
        int32_t  off_dat;
        uint32_t n_files;
} __attribute((packed)) pako_header_t;

typedef struct {
        int32_t off_fname;
        uint32_t fsize;
        int32_t off_cnt;
        uint64_t checksum;
} __attribute((packed)) file_e;

uint64_t htonll(uint64_t value) {
    int num = 42;
    if (*(char *)&num == 42) {
        uint32_t high_part = htonl((uint32_t)(value >> 32));
        uint32_t low_part = htonl((uint32_t)(value & 0xFFFFFFFFLL));
        return (((uint64_t)low_part) << 32) | high_part;
    } else {
        return value;
    }
}

pako_header_t ex;
char content[30000000];

bool check(int fd, uint64_t checksum, uint32_t fsize, int32_t offset){
    bool padding = false;
    int segnum = fsize/8;
    if(fsize%8!=0){
        segnum++;
        padding = true;
    }
    // printf("fsize %d\n", fsize);
    // printf("segnum %d\n", segnum);
    uint64_t sum;
    uint32_t ss = fsize;
    lseek(fd, ex.off_dat + offset, SEEK_SET);
    for(int i=0; i<segnum; i++){
        uint64_t temp = 0;
        if(ss < 8){
            read(fd, &temp, ss);
        }
        else{
            read(fd, &temp, 8);
            ss = ss-8;
        }
        // printf("temp = %lx\n", temp);
        uint64_t temp2 = temp;
        // if(padding == true && i==segnum-1){
        //     for(uint32_t j = ss; j < 8; j++){
        //         temp2 = temp2 * 256;
        //     }
        //     temp = temp2;
        //     printf("aftr = %lx\n", temp);
        // }
        if(i==0){
            sum = temp;
            continue;
        }
        sum = sum ^ temp;
    }
    // printf("sum = %lx\n", sum);
    // printf("checksum = %lx\n", htonll(checksum));
    if(sum == htonll(checksum)){
        // printf("checksum ok\n");
        return true;
    }
    return false;
}
int main(int argc, char *argv[])
{
    int fd;
    fd = open(argv[1], O_RDWR);
    // printf("%d\n", fd);
    if(fd == -1){
        perror("open");
        exit(1);
    }
    // lseek(fd, 0, SEEK_SET);
    int fsize = read(fd, &ex, 16);
    // printf("fsize = %d\n", fsize);
    if(ex.magic[0] == 'P' && ex.magic[1] == 'A' && ex.magic[2] == 'K' &&ex.magic[3] == 'O'){
        printf("Read pako title successfully\n");
    } 
    printf("file offset of the string section: %d\n", ex.off_str);
    printf("file offset of the content section: %d\n", ex.off_dat);
    printf("num of files: %d\n", ex.n_files);
    printf("off_fnm   fsize   off_cnt  checksum\n");
    file_e files[40];
    for(int i=0; i<ex.n_files; i++){
        fsize = read(fd, &files[i], 20);
        files[i].fsize = htonl(files[i].fsize);
        // files[i].checksum = htonll(files[i].checksum);
        printf("%d        ", files[i].off_fname);
        printf("%d        ", files[i].fsize);
        printf("%d        ", files[i].off_cnt);
        printf("%lx\n", htonll(files[i].checksum));
    }
    
    int namesize[40];
    int n = 0, nsize = 0; //n -> filenumber nsize -> filename size
    lseek(fd, ex.off_str, SEEK_SET);
    while(1){
        char a;
        if(n == ex.n_files){
            break;
        }
        read(fd, &a, 1);
        if(a == '\0'){
            namesize[n] = nsize;
            // printf("%d\n", nsize);
            nsize = 0;
            n++;
            lseek(fd, ex.off_str + files[n].off_fname, SEEK_SET);
        }
        nsize++;
    }
    // for(int i = 0; i < ex.n_files; i++) {
    //     printf("%d\n", namesize[i]);
    // }
    int num;
    char filename[40][100];
    for(int i=0; i<ex.n_files; i++){
        lseek(fd, ex.off_str + files[i].off_fname, SEEK_SET);
        read(fd, &filename[i], namesize[i]);
        printf("%s      %d\n", filename[i], files[i].fsize);
        bool ch = check(fd, files[i].checksum, files[i].fsize, files[i].off_cnt);
        if(ch){
            char path[100];
            int len = sizeof(argv[2])/sizeof(argv[2][0]);
            printf("len = %d\n", len);
            for(int j = 0; j < len-1; j++){
                path[j] = argv[2][j];
            }
            path[len-1] = '/';
            for(int j = 0; j < namesize[i]; j++){
                path[len+j] = filename[i][j];
            }
            printf("path: %s\n", path);
            lseek(fd, ex.off_dat+files[i].off_cnt, SEEK_SET);
            read(fd, &content, files[i].fsize);
            int dest = open(path, O_CREAT, S_IRWXU);
            dest = open(path, O_RDWR);

            write(dest, &content, files[i].fsize);
            close(dest);
        }
    }
    // //checksum
    // for(int i=0; i<ex.n_files; i++){
        
    // }
    close(fd);
    return 0;
}
