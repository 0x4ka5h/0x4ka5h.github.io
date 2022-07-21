#include <stdio.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <error.h>
#include <stdlib.h>
#include <errno.h>
#include <limits.h>
#include <unistd.h>
#include <string.h>
#include "linux/input.h"

#define INPUT_DEV_NODE "/dev/input/by-path/platform-ffc04000.i2c-event"
#define SYSFS_DEVICE_DIR "/sys/devices/platform/soc/ffc04000.i2c/i2c-0/0-0053/"

#define EV_CODE_X (0)
#define EV_CODE_Y (1)
#define EV_CODE_Z (2)

#define LOOP_COUNT (1000)

void write_sysfs_cntl_file(const char *dir_name, const char *file_name,
		const char *write_str) {

	char path[PATH_MAX];
	int path_length;
	int file_fd;
	int result;

	// create the path to the file we need to open
	path_length = snprintf(path, PATH_MAX, "%s/%s",	dir_name, file_name);
	if(path_length < 0)
		error(1, 0, "path output error");
	if(path_length >= PATH_MAX)
		error(1, 0, "path length overflow");

	// open the file
	file_fd = open(path, O_WRONLY | O_SYNC);
	if(file_fd < 0)
		error(1, errno, "could not open file '%s'", path);
	
	// write the string to the file
	result = write(file_fd, write_str, strlen(write_str));
	if(result < 0)
		error(1, errno, "writing to '%s'", path);
	if((size_t)(result) != strlen(write_str))
		error(1, errno, "buffer underflow writing '%s'", path);

	// close the file
	result = close(file_fd);
	if(result < 0)
		error(1, errno, "could not close file '%s'", path);
}

int main(void) {
	int event_dev_fd;
	const char *input_dev_node = INPUT_DEV_NODE;
	int result;
	int i;
	int loop;
	struct input_event the_event;
	struct input_absinfo the_absinfo;
	int abs_value_array[3] = {0};

	int last_value_x=0;
	int last_value_y=0;
	int last_value_z=0;
	int x_abs_value_array=0;
	int y_abs_value_array=0;
	int z_abs_value_array=0;
	int check=1;
	
	system("chmod 777 /sys/class/gpio/export");
	system("echo 107 > /sys/class/gpio/export");
	system("echo out > /sys/class/gpio/gpio107/direction");
	system("echo 1 > /sys/class/gpio/gpio107/value");

	// enable adxl
	write_sysfs_cntl_file(SYSFS_DEVICE_DIR, "disable", "0");

	// set the sample rate to maximum
	write_sysfs_cntl_file(SYSFS_DEVICE_DIR, "rate", "15");

	// do not auto sleep
	write_sysfs_cntl_file(SYSFS_DEVICE_DIR, "autosleep", "0");
	
	// open the event device node
	event_dev_fd = open(input_dev_node, O_RDONLY | O_SYNC);
	if(event_dev_fd < 0)
		error(1, errno, "could not open file '%s'", input_dev_node);
	
	// read the current state of each axis
	printf("\n");
	for(i = 0 ; i < 3 ; i++ ) {
		result = ioctl (event_dev_fd, EVIOCGABS(i), &the_absinfo);
		if(result < 0)
			error(1, errno, "ioctl from '%s'", input_dev_node);
		
	}
	
	fflush(stdout);

	

	// read the next LOOP_COUNT events
	for(loop = 0 ;; loop++) {
		// read the next event
		result = read(event_dev_fd, &the_event, 
				sizeof(struct input_event));
		if(result < 0)
			error(1, errno, "reading %d from '%s'", 
					sizeof(struct input_event),
					input_dev_node);
		if(result != sizeof(struct input_event))
			error(1, 0, "did not read %d bytes from '%s'", 
					sizeof(struct input_event),
					input_dev_node);

		// read the current state of each axis
		for(i = 0 ; i < 3 ; i++ ) {
			result = ioctl (event_dev_fd, EVIOCGABS(i), 
					&the_absinfo);
			if(result < 0)
				error(1, errno, "ioctl from '%s'",
						input_dev_node);
				
			abs_value_array[i] = the_absinfo.value;
		}
		if (last_value_x!=0 || last_value_y!=0 || last_value_y!=0){
			if (((abs(abs_value_array[0]-last_value_x))>200 || (abs(abs_value_array[1]-last_value_y))>200) && ((abs(abs_value_array[0]-last_value_x))>200 || (abs(abs_value_array[2]-last_value_z))>200) && ((abs(abs_value_array[1]-last_value_y))>200 || (abs(abs_value_array[2]-last_value_z))>200)){
printf("%d\n",abs(abs_value_array[0]-last_value_x));
printf("%d\n",abs(abs_value_array[1]-last_value_y));
printf("%d\n",abs(abs_value_array[2]-last_value_z));
printf(" -- %d,%d,%d ----- \n",
					abs_value_array[0],
					abs_value_array[1],
					abs_value_array[2]
					);
			system("echo 0 > /sys/class/gpio/gpio107/value");
			printf(" ------------  accident occurs ----------\n");
			
			break;
			
			}

		if((abs(abs_value_array[0]-last_value_x))>300 || (abs(abs_value_array[1]-last_value_y))>300 || (abs(abs_value_array[2]-last_value_z))>300){
			printf("%d\n",abs(abs_value_array[0]-last_value_x));
printf("%d\n",abs(abs_value_array[1]-last_value_y));
printf("%d\n",abs(abs_value_array[2]-last_value_z));
			printf(" ------------- %d,%d,%d ----------------- \n",
					abs_value_array[0],
					abs_value_array[1],
					abs_value_array[2]
					);
			system("echo 0 > /sys/class/gpio/gpio107/value");
			printf(" ------------  accident occurs ----------\n");
			break;
			
			}
		
		}
		
		if (check%50==0){

			last_value_x = abs_value_array[0];
			last_value_y = abs_value_array[1];
			last_value_z = abs_value_array[2];
			printf("%d,%d,%d ----------------- \n",
					abs_value_array[0],
					abs_value_array[1],
					abs_value_array[2]
					);
			check++;
		}
		if (x_abs_value_array!=abs_value_array[0] && y_abs_value_array!=abs_value_array[1] && z_abs_value_array!=abs_value_array[2] ){
			check++;
			printf("%d,%d,%d --- %d\n",
					abs_value_array[0],
					abs_value_array[1],
					abs_value_array[2],
					check);
		}

		x_abs_value_array = abs_value_array[0];
		y_abs_value_array = abs_value_array[1];
		z_abs_value_array = abs_value_array[2];
		
	}
	

	result = close(event_dev_fd);
	if(result < 0)
		error(1, errno, "could not close file '%s'", input_dev_node);

	// disable adxl
	write_sysfs_cntl_file(SYSFS_DEVICE_DIR, "disable", "1");
}

