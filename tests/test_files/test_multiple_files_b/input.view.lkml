view: orders {
  sql_table_name: `my_project.dataset.orders` ;;
  
  dimension: a_dimension_name {
    type: number
  }
  
  measure: a_measure_name {
    type: average
  }

  filter: a_filter_name {
    type: number
  }
}
