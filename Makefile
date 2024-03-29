##
## EPITECH PROJECT, 2023
## B-CNA-500-REN-5-1-graphanalysis-nicolas.deschaseaux
## File description:
## Makefile
##

SRC = ./ia.py
MODULES = ./src/pisqpipe.py ./src/annexe_function.py

NAME = pbrain-gomoku-ai

all: $(NAME)

$(NAME): $(SRC) 
	cp $(SRC) $(NAME)
	echo "#!/usr/bin/env python3" | cat - $(NAME) > temp && mv temp $(NAME)
	chmod a+x $(NAME)

clean:

fclean: clean
	rm -f $(NAME)

re: fclean all

.PHONY: all clean fclean re
