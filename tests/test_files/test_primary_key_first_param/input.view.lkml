view: orders {
  sql_table_name: `my_project.dataset.orders` ;;

  filter: a_filter_name {
    type: number
  }

  dimension: a_dimension_name {
    type: number
  }

  dimension: b_dimension_name {
    type: number
    primary_key: yes
  }

  measure: a_measure_name {
    type: average
  }
}
