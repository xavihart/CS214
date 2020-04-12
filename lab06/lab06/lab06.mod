/*********************************************
 * OPL 12.9.0.0 Model
 * Author: HP
 * Creation Date: 2020年4月11日 at 下午11:38:26
 *********************************************/
int Num_of_product = ...;
int Num_of_machines = ...;
int Num_of_month = ...;
int Num_of_days = ...;
int Store_limination = ...;
int Kind_of_machines = ...;
float hold_cost = ...;

float hours_in_a_day = ...;

range num_of_product = 1..Num_of_product;
range num_of_machines = 1..Num_of_machines;
range num_of_month = 1..Num_of_month;
range kind = 1..Kind_of_machines;
 
 
float time[num_of_product][kind] = ...;
int market_limit[num_of_product][num_of_month] = ...;
int profit[num_of_product] = ...;
int machine_numbers[kind] = ...;

dvar int machine_used[num_of_month][kind];
dvar int hold[num_of_product][num_of_month];
dvar int make[num_of_product][num_of_month];
dvar int sell[num_of_product][num_of_month];




maximize 
    sum(i in num_of_product, j in num_of_month)
        (sell[i][j] * profit[i] - hold[i][j] * hold_cost);
        
subject to{

     // market limitation
    forall(i in num_of_product)
      forall(j in num_of_month){
        sell[i][j] <= market_limit[i][j];
        hold[i][j] >= 0;
        make[i][j] >= 0;
        sell[i][j] >= 0;
        
      }
      
   // machine maintance   
    forall(i in kind){
       sum(p in num_of_month)
         machine_used[p][i] == machine_numbers[i] * (Num_of_month - 1);    
        forall(j in num_of_month){
            machine_used[j][i] >= 0;   
        }
    }
    
    forall(i in kind)
      forall(j in num_of_month)
        machine_used[j][i] <= machine_numbers[i];
    
    // hold for June is 50 and the limitations for the first month
    forall(p in num_of_product){
        make[p][1] - sell[p][1] == hold[p][1];
        hold[p][1] <= Store_limination;
        hold[p][Num_of_month] == 50;    
    }
           
    // for month 2 to 6       
    forall(p in num_of_product)
    forall(i in 2..Num_of_month){
      make[p][i] + hold[p][i - 1] - sell[p][i] == hold[p][i];
      hold[p][i] <= Store_limination;
    }
    
    
    // working time limitations
    forall(i in num_of_month)
        forall(k in kind){
        ctCapacity: sum(p in num_of_product)  make[p][i] * time[p][k]
         <= machine_used[i][k] * Num_of_days * hours_in_a_day;
    }                         
    

}

   

