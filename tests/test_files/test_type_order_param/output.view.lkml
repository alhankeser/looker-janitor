view: orders {
  sql_table_name: `my_project.dataset.orders` ;;

  measure: a_measure_name {
    type: average
  }

  dimension: a_dimension_name {
    type: number
  }

  filter: a_filter_name {
    type: number
  }
}
