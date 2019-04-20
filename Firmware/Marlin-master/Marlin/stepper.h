/*
  stepper.h - stepper motor driver: executes motion plans of planner.c using the stepper motors
  Part of Grbl

  Copyright (c) 2009-2011 Simen Svale Skogsrud

  Grbl is free software: you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.

  Grbl is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with Grbl.  If not, see <http://www.gnu.org/licenses/>.
*/

#ifndef stepper_h
#define stepper_h 

#include "planner.h"
#include "slave_comms.h"

#ifdef REPRAPPRO_MULTIMATERIALS

#define WRITE_E_STEP(v) { if(current_block->active_extruder == 2) { slaveRemoteStep(2, v); } else { if(current_block->active_extruder == 1) { slaveRemoteStep(1, v); } else { WRITE(E0_STEP_PIN, v); }}}
#define NORM_E_DIR() { if(current_block->active_extruder == 2) { slaveRemoteDir(2, true); } else { if(current_block->active_extruder == 1) { slaveRemoteDir(1, true); } else { WRITE(E0_DIR_PIN, !INVERT_E0_DIR); }}}
#define REV_E_DIR() { if(current_block->active_extruder == 2) { slaveRemoteDir(2, false); } else { if(current_block->active_extruder == 1) { slaveRemoteDir(1, false); } else { WRITE(E0_DIR_PIN, INVERT_E0_DIR); }}}


/*
inline void WRITE_E_STEP(int8_t v) 
{ 
	if(current_block->active_extruder == 2) 
	{ 
		slaveRemoteStep(2, v);  //E2_STEP_PIN, v); 
	} else 
	{ 
		if(current_block->active_extruder == 1) 
		{ 
			slaveRemoteStep(1, v); //E1_STEP_PIN, v); 
		} else 
		{ 
			WRITE(E0_STEP_PIN, v); 
		}
	}
}

inline void NORM_E_DIR() 
{ 
	if(current_block->active_extruder == 2) 
	{ 
		slaveRemoteDir(2, true); //!E2_DIR_PIN, INVERT_E2_DIR); 
	} else 
	{ 
		if(current_block->active_extruder == 1) 
		{ 
			slaveRemoteDir(1, true); //!E1_DIR_PIN, INVERT_E1_DIR); 
		} else 
		{ 
			WRITE(E0_DIR_PIN, !INVERT_E0_DIR); 
		}
	}
}

inline void REV_E_DIR() 
{ 
	if(current_block->active_extruder == 2) 
	{ 
		slaveRemoteDir(2, false); //E2_DIR_PIN, INVERT_E2_DIR); 
	} else 
	{ 
		if(current_block->active_extruder == 1) 
		{ 
			slaveRemoteDir(1, false); //E1_DIR_PIN, INVERT_E1_DIR); 
		} else 
		{ 
			WRITE(E0_DIR_PIN, INVERT_E0_DIR); 
		}
	}
}
*/
#else

#if EXTRUDERS > 2
  #define WRITE_E_STEP(v) { if(current_block->active_extruder == 2) { WRITE(E2_STEP_PIN, v); } else { if(current_block->active_extruder == 1) { WRITE(E1_STEP_PIN, v); } else { WRITE(E0_STEP_PIN, v); }}}
  #define NORM_E_DIR() { if(current_block->active_extruder == 2) { WRITE(!E2_DIR_PIN, INVERT_E2_DIR); } else { if(current_block->active_extruder == 1) { WRITE(!E1_DIR_PIN, INVERT_E1_DIR); } else { WRITE(E0_DIR_PIN, !INVERT_E0_DIR); }}}
  #define REV_E_DIR() { if(current_block->active_extruder == 2) { WRITE(E2_DIR_PIN, INVERT_E2_DIR); } else { if(current_block->active_extruder == 1) { WRITE(E1_DIR_PIN, INVERT_E1_DIR); } else { WRITE(E0_DIR_PIN, INVERT_E0_DIR); }}}
#elif EXTRUDERS > 1
  #define WRITE_E_STEP(v) { if(current_block->active_extruder == 1) { WRITE(E1_STEP_PIN, v); } else { WRITE(E0_STEP_PIN, v); }}
  #define NORM_E_DIR() { if(current_block->active_extruder == 1) { WRITE(E1_DIR_PIN, !INVERT_E1_DIR); } else { WRITE(E0_DIR_PIN, !INVERT_E0_DIR); }}
  #define REV_E_DIR() { if(current_block->active_extruder == 1) { WRITE(E1_DIR_PIN, INVERT_E1_DIR); } else { WRITE(E0_DIR_PIN, INVERT_E0_DIR); }}
#else
  #define WRITE_E_STEP(v) WRITE(E0_STEP_PIN, v)
  #define NORM_E_DIR() WRITE(E0_DIR_PIN, !INVERT_E0_DIR)
  #define REV_E_DIR() WRITE(E0_DIR_PIN, INVERT_E0_DIR)
#endif

#endif



// Initialize and start the stepper motor subsystem
void st_init();

// Block until all buffered steps are executed
void st_synchronize();

// Set current position in steps
void st_set_position(const long &x, const long &y, const long &z, const long &e);
void st_set_e_position(const long &e);

// Get current position in steps
long st_get_position(uint8_t axis);

// The stepper subsystem goes to sleep when it runs out of things to execute. Call this
// to notify the subsystem that it is time to go to work.
void st_wake_up();

  
void checkHitEndstops(); //call from somwhere to create an serial error message with the locations the endstops where hit, in case they were triggered
void endstops_hit_on_purpose(); //avoid creation of the message, i.e. after homeing and before a routine call of checkHitEndstops();

void enable_endstops(bool check); // Enable/disable endstop checking

void checkStepperErrors(); //Print errors detected by the stepper

void finishAndDisableSteppers();

extern block_t *current_block;  // A pointer to the block currently being traced
extern volatile long endstops_trigsteps[];
extern volatile bool endstop_z_hit;
extern bool old_z_min_endstop;

void quickStop();
#endif
