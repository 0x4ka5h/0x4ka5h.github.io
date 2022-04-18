#include <stdlib.h>
#include <stdio.h>
int main(){
	FILE *fptr;
	int i;
	system("echo 108 > /sys/class/gpio/export");
	system("echo in > /sys/class/gpio/gpio108/direction");
	system("echo 1 > /sys/class/gpio/gpio108/value");
	while (1){
		if (system("cat /sys/class/gpio/gpio108/value > s.txt")){
			printf("oo");
			fptr = fopen("s.txt","r");
			fscanf(fptr,"%d",i);
			printf("%d",i);
			if (i==0){
				printf("restarted");
				system("./watch");			
			}

		}
	}

}
