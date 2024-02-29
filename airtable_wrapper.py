from pyairtable import Api
from pyairtable.formulas import match
import logging



class Airtable:
    def __init__(self, airtable_token, airtable_base_id, airtable_table_id, airtable_fields) -> None:
        self.api = Api(airtable_token)
        self.table = self.api.table(airtable_base_id, airtable_table_id)
        self.airtable_fields = airtable_fields
    
    
    def validate_fields(self, 
                        field_values: dict) -> bool:
        """Utility function to check if the dictionary of field values 
           provided does not contain any invalid fields

        Args:
            field_values (dict): The field values provided

        Returns:
            boolean: True if the dictionary is valid, False otherwise
        """
        
        for field in list(field_values.keys()):
            if field not in self.airtable_fields:
                logging.error('Invalid field provided when creating new record')
                return False
        return True
        
        
    def get_all_records(self):
        """Returns all of the records in the table as a string"""
        output = ''
        
        for record in self.table.all():
            fields = record['fields']
            
            for field_name, field_value in fields.items():
                output += f'{field_name}: {field_value};'
            
            output += '\n'
        
        return output

    
    def create_record(self,
                      field_values: dict):
        """Create a new record and add it to the airtable

        Args:
            field_values (dict): Dictionary with key value pairs for fields and values
        """
        
        if self.validate_fields(field_values): 
            try:
                #if all fields are valid, simply add the dictionary to the table
                self.table.create(field_values)
                logging.info('Created record successfully')
                return True
            except Exception as e:
                logging.error(e)
        
        return False
                
                
    def update_record(self, 
                      formula: dict, 
                      field_values: dict):
        """Update existing record in the table with the field values provided

        Args:
            formula (dict): dictionary for the formula to identify the record that needs to be updated
            field_values (dict): dictionary with the fields to be changed and their values
        """
        
        if self.validate_fields(field_values):
            #get the record to be deleted to extract its id
            target_record = self.table.first(formula=match(formula))
            
            if target_record:
                #only try update if record exists
                self.table.update(target_record['id'], field_values, replace=False)
                logging.info(f'Updated record successfully for {formula}')
                return True
            else:
                logging.error('Tried to update record which does not exist')
                return False 
            
    
    def delete_record(self, formula):
        """Delete existing record by primary key

        Args:
            primary_key (string): Primary key of business for record getting deleted
        """
        
        #get the record to be deleted to extract its id
        target_record = self.table.first(formula=match(formula))
        
        if target_record:
            self.table.delete(target_record['id'])
            logging.info(f'Deleted record successfully for {formula}')
            return True
        else:
            logging.error('Tried to delete record which does not exist')
            return False
        
    
    
    
if __name__ == '__main__':
    airtable = Airtable()
    airtable.delete_record('New business')


