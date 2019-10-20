#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int main(void)
{
	int i, r;

	srand(time(0));

	FILE *output = fopen("output.txt", "w");

	for (i = 0; i < 30; i++)
	{
		r = rand() & 0xf;
		fprintf(output, "%d\n", r);
	}

	fclose(output);
}
