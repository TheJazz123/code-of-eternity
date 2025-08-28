from termcolor import colored
#data files

realms = {
    'scriptoria central': {
        'name': 'Scriptoria Central',
        'locations': {
            'start': {
                'description': "You're at the entrance of Scriptoria.",
                'items': ['bag'],
                'exits': {'north': 'hall', 'south': 'garden'},
                'coords': (0, 0)
            },
            'hall': {
                'description': "You're in a grand hall with tall pillars.",
                'items': ['debug','cipheras note'],
                'exits': {'north': 'loop labyrinth','south':'start', 'west': 'code fountain'},
                'coords': (0, 1)
            },
            'garden': {
                'description': "You're in a serene garden.",
                'items': ['scriptoria crystal'],
                'exits': {'north': 'start','east': 'binary balcony'},
                'coords': (0, -1),
                'teleport_station': 'pixel pond'
                
            },
            'cryptic cave': {
                'description': "You've entered a dark cave with glowing scripts on the walls.",
                'items': ['challengers orb'],
                'exits': {'east': 'code fountain'},
                'coords': (-2,1)
            },
            'pixel pond': {
                'description': "A serene pond with pixels shimmering beneath the surface.",
                'items': ['a coding tome'],
                'exits': {},
                'coords': (-1,-2),
                'teleport_station': 'garden'
            },
            'algorithm arena': {
                'description': "A vast arena where the greatest algorithms battle for efficiency.",
                'items': [],
                'exits': {},  
                'coords': (2,0),
                'teleport_station': 'binary balcony',
                'transition_gate': 'Syntax Gateway',
                'guardian challenge': {
            'completed': True
                }
            },
            'loop labyrinth': {
                'description': "A twisting maze where loops can trap the unwary forever.",
                'items': [],
                'exits': {'south': 'hall'},  
                'coords': (0,2),
                'transition_gate': 'Central Portal',
                'guardian challenge': {
            'completed': False,
            'guardian': 'Script Keeper',
            'intro': ["\nWelcome, traveler of bytes and bits, to the heart of Scriptoria!",
        f"I am the {colored('Script Keeper','red')}, guardian of ancient tales.",
        "These halls archive our history and future dreams.",
        f"To pass my gate, {colored('solve a riddle','blue')} that has stumped many.",
        f"Prove your worth, and {colored('you shall gain passage','green')}."],
            'challenge': '''Guardian Challenge: Riddle

The Script Keeper awaits your answer.

I'm no spy, but I watch you all the time.
I capture moments, both mundane and sublime.
I have no memories, yet I store thousands,
Frozen as they were.''',
            'answer': ['camera'],
            'victory': "With words, you've woven the way forward. Tread triumphantly!",
            'defeat': "Riddles wrap reality in mystery. Ponder and proceed."
        },
            },
            'echo cave': {
                'description': "Every sound you make echoes back, but not always as you expect.",
                'items': ['a mysterious key'],
                'exits': {},
                'coords': (2,-2),
                'teleport_station': 'binary balcony'
            },
            'code fountain': {
                'description': "A sparkling fountain of pure code, flowing endlessly.",
                'items': [],
                'exits': {'west': 'cryptic cave', 'east': 'hall'},
                'coords': (-1,1)
            },
            'binary balcony': {
                'description': "A balcony overlooking a vast landscape of 0s and 1s.",
                'items': [],
                'exits': {'west': 'garden'},
                'coords': (1,-1),
                'teleport_station': 'echo cave'
            }
        }
    },
    'recursive realm': {
        'name': 'Recursive Realm',
        'locations': {
            'recursion riviera': {
                'description': "A shimmering coastline where the waves seem to recede and advance in a never-ending cycle.",
                'items': [],
                'exits': {'north': 'function forest', 'west': 'loop lagoon'},
                'coords': (0,0)
            },
            'function forest': {
                'description': "Dense woods where trees represent various functions, and their intertwining roots symbolize deep recursive connections.",
                'items': [],
                'exits': {'west': 'base case beach','east': 'call stack cliffs'},
                'coords': (0,1)
            },
            'loop lagoon': {
                'description': "A serene water body that loops around itself in a peculiar pattern, with the water flowing back to its source.",
                'items': [],
                'exits': {'north': 'base case beach','south': 'fractal fountain'},
                'coords': (-1,0)
            },
            'base case beach': {
                'description': "A tranquil beach where recursion enthusiasts find their base cases and break from endless loops.",
                'items': [],
                'exits': {'east': 'function forest','south': 'loop lagoon'},
                'coords': (-1,1)
            },
            'call stack cliffs': {
                'description': "Towering cliffs representing layers of function calls. One must be careful not to overflow here!",
                'items': [],
                'exits': {'west': 'function forest'},
                'coords': (1,1),
                'teleport_station': 'tail trench'
            },
            'tail trench': {
                'description': "A deep trench symbolic of tail recursion. It has a mysterious depth but optimizes the space around.",
                'items': [],
                'exits': {'south': 'memoization meadows'},  
                'coords': (2,0),
                'teleport_station': 'call stack cliffs',
                'transition_gate': 'Recursive Doorway',
                'guardian challenge': {
            'completed': False,
            'guardian': 'Recursion Ruler',
            'intro': ["\nAh, seeker of cycles, welcome to the enigmatic lands of the Recursive Realm!",
        "I am the Recursion Ruler, lord of loops that spiral endlessly into the infinity of code.",
        "In my domain, everything that begins is destined to circle back to its origin, echoing in an endless loop.",
        "Such is the nature of recursion.",
        "Before you venture deeper into my realm's spirals, you must prove your depth of understanding by deciphering a snippet of code I present.",
        "Only those deemed worthy may proceed."],
            'challenge': '''Guardian Challenge: Code Decipher
The guardian presents you with a script etched in light

def puzzling_function(x, y):
    if x == 0:
        return y + 1
    elif x > 0 and y == 0:
        return puzzling_function(x-1, 1)
    elif x > 0 and y > 0:
        return puzzling_function(x-1, puzzling_function(x, y-1))

What function does it represent?
            ''',
            'answer': ['ackermann function','ackermann'],
            'victory': "Bravo! You've untangled the threads of code with mastery.",
            'defeat': "Coding challenges confound even the craftiest. Reassess and retry."
        }
    },
            'memoization meadows': {
                'description': "Lush fields where previously computed values are stored, preventing unnecessary work.",
                'items': [],
                'exits': {'north': 'tail trench', 'west': 'iterative inn'},
                'coords': (2,-1)
            },
            'iterative inn': {
                'description': "A cozy inn for those who sometimes want a break from recursion and prefer iteration.",
                'items': [],
                'exits': {'east': 'memoization meadows'},
                'coords': (1,-1)
            },
            'dynamic dale': {
                'description': "A valley showcasing the dance between dynamic programming and recursion, with patterns revealing optimized solutions.",
                'items': [],
                'exits': {},
                'coords': (0,-2),
                'teleport_station': 'fractal fountain',
                'transition_gate': 'Central Portal',
                'guardian challenge': {
            'completed': True
                }
            },
            'fractal fountain': {
                'description': "A magical fountain with water sprouting in intricate fractal patterns. Observers often ponder the nature of recursion here.",
                'items': [],
                'exits': {'north': 'loop lagoon'},
                'coords': (-1,-1),
                'teleport_station': 'dynamic dale'
            }
        }
    },
    'binary battlegrounds': {
        'name': 'Binary Battlegrounds',
        'locations': {
            'bit bastion': {
                'description': "A fortress built from shining bits, alternating between 0s and 1s.",
                'items': [],
                'exits': {},  
                'coords': (0,-2),
                'transition_gate': 'Binary Bridge',
                'teleport_station': 'overflow oasis',
                'guardian challenge': {
            'completed': False,
            'guardian': 'Binary Baron',
            'intro': ["\nGreetings, voyager of variables! You tread now upon the Binary Battlegrounds, where every conflict is resolved in black and white, zeroes and ones.",
        "I am the Binary Baron, master of dichotomies and the dual nature of digital life.",
        "Here, choices are stark, and there's no middle ground.",
        "To earn my respect and the key to the next realm, you must navigate through the logical challenges that define my dominion.",
        "Are you ready to face the duality?"],
            'challenge': '''Guardian Challenge: Logic Gates Puzzle
The Binary Baron has conjured a complex logic gate sequence!
Gates: AND -> NOR -> XOR -> NOT")
Instructions:
1. Two switches (A and B) control the input to the AND gate.")
2. The output from the AND gate, along with Switch C, controls the NOR gate.
3. The output from the NOR gate, along with Switch D, controls the XOR gate.")
4. Finally, the output from the XOR gate goes through a NOT gate.")
5. Your goal is to make the final output '1'.")
You must set the switches (0 for OFF, 1 for ON) correctly to solve the puzzle.

Provide your values for switches A,B,C,D separated by commas.''',
            'answer': ['0, 0, 0, 1', '0, 0, 1, 0', '0, 1, 0, 1', '0, 1, 1, 0', '1, 0, 0, 1', '1, 0, 1, 0'],
            'victory': "You've illuminated the path with logic and wit! Proceed with pride.",
            'defeat': "The circuits of challenge sometimes befuddle. Reflect and return."

        }
    },
            'logic lane': {
                'description': "A pathway where logical operators converse in boolean whispers.",
                'items': [],
                'exits': {'north': 'byte boulevard'},
                'coords': (-1,-1)
        },
            'byte boulevard': {
                'description': "A wide road adorned with statues of famous bytes from computing history.",
                'items': [],
                'exits': {'west': 'shift stronghold', 'east': 'logic gate grove', 'south':'logic lane'},
                'coords': (-1,0)
        },
            'shift stronghold': {
                'description': "A towering keep where bits shift left and right, adjusting their positions.",
                'items': [],
                'exits': {'east': 'byte boulevard' },
                'coords': (-2,0),
                'transition_gate': 'Recursive Doorway',
                    'guardian challenge': {
                'completed': True
                    }
        },
            'logic gate grove': {
                'description': "A serene garden filled with gates – AND, OR, NOT – that guide the flow of logic.",
                'items': [],
                'exits': {'north': 'twos complement cove','west': 'byte boulevard'},
                'coords': (0,0)
        },
            'twos complement cove': {
                'description': "A secluded bay where numbers lounge in their positive and negative forms.",
                'items': [],
                'exits': {'south': 'logic gate grove', 'east': 'endian estate' },
                'coords': (0,1)
        },
            'endian estate': {
                'description': "A grand mansion where little-endians and big-endians debate over byte order.",
                'items': [],
                'exits': {'west': 'twos complement cove'},
                'coords': (1,1),
                'teleport_station': 'hex haven'
        },
            'hex haven': {
                'description': "A sanctuary for numbers that prefer a base of 16, gleaming in hexadecimal hues.",
                'items': [],
                'exits': {'south': 'parity plaza'},
                'coords': (2,0),
                'teleport_station': 'endian estate'
        },
            'parity plaza': {
                'description': "A square where even and odd bits gather to ensure data integrity.",
                'items': [],
                'exits': {'north': 'hex haven', 'west': 'overflow oasis'},
                'coords': (2,-1)
        },
            'overflow oasis': {
                'description': "A refreshing pool in the desert where bits occasionally spill over in exuberance.",
                'items': [],
                'exits': {'east': 'parity plaza'},
                'coords': (1,-1),
                'teleport_station': 'bit bastion'
        }
        }
    },
    'variable valleys': {
        'name': 'Variable Valleys',
        'locations': {
            'scope springs': {
                'description': "A rejuvenating spring where local and global scopes merge and create magic.",
                'items': [],
                'exits': {'east': 'numeric nook'},  
                'coords': (-2,0),
                'transition_gate': 'Syntax Gateway',
                'guardian challenge': {
            'completed': False,
            'guardian': 'Syntax Sovereign',
            'intro': ["\nSalutations, wanderer of the winding ways! You've entered the Variable Valleys, where everything changes like the shifting sands.",
        "I am the Syntax Sovereign, keeper of constants in a land of change.",
        "Here, the landscape shifts with the winds of whim, and only those with keen minds can chart a steady course.",
        "To validate your vision and verify your virtue, you must solve a conundrum that I have crafted.",
        "Only then may you venture forth into the ever-shifting sands."],
            'challenge': '''Guardian Challenge: Rearrange
Rearrange my fragments to unlock the path forward.

finite ... deterministic ... of ... automaton ... accepts ... a ... by ...
string ... sequence ... A ... states

The code fragments before you seem to describe a foundational concept in computing.
''',
            'answer': ['a deterministic finite automaton accepts a string by sequence of states'],
            'victory': "Impressive! You've stitched together the fabric of memory with elegance and ease.",
            'defeat': "Even the strongest minds sometimes falter. Try again, seeker."

        }
    },
            'immutable isle': {
                'description': "A steadfast island where nothing ever changes, reminding coders of constants.",
                'items': [],
                'exits': {'north': 'string stream', 'west': 'numeric nook'}, 
                'coords': (0,0)
            },
            'string stream': {
                'description': "A serene stream where soft ripples look like strings of text flowing through the waters.",
                'items': [],
                'exits': {'north': 'dictionary delta', 'south': 'immutable isle', 'west': 'tuple terrace','east': 'boolean bluffs'}, 
                'coords': (0,1)
            },
            'boolean bluffs': {
                'description': "Towering cliffs with binary patterns, signifying true and false pathways.",
                'items': [],
                'exits': {'west': 'string stream'}, 
                'coords': (1,1),
                'teleport_station': 'list lagoon'
            },
            'numeric nook': {
                'description': "A cozy corner filled with counting, from integers to floating wonders.",
                'items': [],
                'exits': {'north': 'tuple terrace', 'west': 'scope springs','east': 'immutable isle'}, 
                'coords': (-1,0)
            },
            'array archipelago': {
                'description': "A cluster of islands, each representing elements of an array in a sequence.",
                'items': [],
                'exits': {'east': 'set summit'}, 
                'coords': (1,-1)
            },
            'tuple terrace': {
                'description': "A terraced area showcasing ordered immutables, where each step resembles tuple elements.",
                'items': [],
                'exits': {'east': 'string stream','south': 'numeric nook'}, 
                'coords': (-1,1)
            },
            'list lagoon': {
                'description': "A vast waterbody, signifying dynamic size and versatility of lists.",
                'items': [],
                'exits': {'south': 'set summit'},
                'coords': (2,0),
                'teleport_station': 'boolean bluffs'
            },
            'set summit': {
                'description': "The peak where no duplicate element is found, signifying unique values.",
                'items': [],
                'exits': {'north': 'list lagoon', 'west': 'array archipelago'},
                'coords': (2,-1)
            },
            'dictionary delta': {
                'description': "A river's end, where key-value pairs determine the flow of water.",
                'items': [],
                'exits': {'south': 'string stream'}, 
                'coords': (0,2),
                'transition_gate': 'Binary Bridge',
                'guardian challenge': {
            'completed': True
            }
            }
        }
    },
    '' : {
        'name': '',
        'locations': {

        }
    }
}

items = {
    'a mysterious key': 'An old, rusty key with an emblem of a quill on it.',
    'a coding tome': 'An ancient book filled with coding wisdom of the past.',
    'scriptoria crystal': 'A shimmering crystal emanating a gentle light, \n\
believed to be the key to the hidden teleport stations within Scriptoria Central.',
    'recursive crystal': 'A looping crystal, spiraling into itself endlessly. \n\
It holds the power to navigate the intricate pathways of the Recursive Realm.',
    'binary crystal': 'A two-faced gem, constantly flipping between its facets. \n\
It unlocks the a few regions of the Binary Battlegrounds.',
    'variable crystal': 'A mutable, shimmering vial that constantly shifts in hue and shape.\n\
 It\'s said to guide one through the ever-changing landscapes of Variable Valleys.',
    'universal teleporter': 'A sleek device, adorned with multi-colored gems that glow intermittently. \n\
It\'s believed to allow instantaneous travel to known locations.',
    'debug':'A strange device that restores your state to a cleaner version and replenishes HP.',
    'cipheras note':'A note dropped by Ciphera.',
    'challengers orb':'An orb that lets you take on the guardian challenges and travel across realms.',
    'ottos shop':'Otto has the latest wares as long as you have the coin.'
}

realm_transitions = {
    'loop labyrinth': {
        'enter': 'dynamic dale',
        'realm': 'recursive realm'
        },
    'dynamic dale': {
        'enter': 'loop labyrinth',
        'realm': 'scriptoria central'
    },
    'algorithm arena': {
        'enter': 'scope springs',
        'realm': 'variable valleys'
        },
    'scope springs': {
        'enter': 'algorithm arena',
        'realm': 'scriptoria central'
    },
    'tail trench': {
        'enter': 'shift stronghold',
        'realm': 'binary battlegrounds'
        },
    'shift stronghold': {
        'enter': 'tail trench',
        'realm': 'recursive realm'
    },
    'bit bastion': {
        'enter': 'dictionary delta',
        'realm': 'variable valleys'
        },
    'dictionary delta': {
        'enter': 'bit bastion',
        'realm': 'binary battlegrounds'
    }
}
