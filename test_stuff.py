def check_for_valid_id(input_id):
    """
    input: input id
    outputs: the input id if it is an integer
    """

    if not isinstance(input_id, int):
        try: 
            return int(input_id)
        except ValueError or TypeError:
            return {
                "message": f"ID {input_id} must be an integer"
            }, 400
    return input_id

#print(check_for_valid_id(5))

input_id = 'pasta'
#print(isinstance(input_id, int))
print(int(input_id))



        